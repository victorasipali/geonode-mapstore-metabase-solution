import json
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .metabase import get_metabase_embed_url


@login_required
def analytics_dashboard(request):
    metabase_url = get_metabase_embed_url(dashboard_id=2, bordered=False, titled=False)
    return render(request, 'metabase/dashboard.html', {
        'metabase_url': metabase_url,
        'page_title': 'Analytics Dashboard'
    })


def themes_catalogue(request):
    from geonode.groups.models import GroupCategory
    from geonode.layers.models import Dataset

    categories = []
    theme_data = {}

    for cat in GroupCategory.objects.all().order_by('name'):
        groups_data = []
        for g in cat.groups.all().order_by('title'):
            layers = Dataset.objects.filter(
                group=g.group
            ).order_by('title')
            layer_list = [
                {
                    'id': l.id,
                    'name': l.name or '',
                    'title': l.title or '',
                    'subtype': l.subtype or 'dataset',
                    'thumb': l.thumbnail_url or '',
                    'url': f'/catalogue/#/dataset/{l.id}'
                }
                for l in layers
            ]
            groups_data.append({
                'profile': g,
                'layers': layers,
                'layer_count': layers.count(),
            })
            theme_data[g.slug] = {
                'title': g.title,
                'cat': cat.name,
                'count': layers.count(),
                'layers': layer_list
            }
        categories.append({
            'category': cat,
            'groups': groups_data,
            'total_layers': sum(gd['layer_count'] for gd in groups_data),
        })

    return render(request, 'themes/catalogue.html', {
        'categories': categories,
        'theme_data_json': json.dumps(theme_data),
        'page_title': 'Browse by Theme',
    })


def feedback_view(request):
    from .feedback import Feedback
    from django.core.mail import send_mail
    from django.conf import settings

    success = False
    error = None

    if request.method == 'POST':
        name = request.POST.get('name', '').strip() or 'Anonymous'
        email = request.POST.get('email', '').strip()
        category = request.POST.get('category', 'general')
        message = request.POST.get('message', '').strip()

        if not message:
            error = 'Please enter a message.'
        else:
            # Get IP
            x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

            # Save to database
            fb = Feedback.objects.create(
                name=name,
                email=email,
                category=category,
                message=message,
                ip_address=ip,
            )

            # Send email notification
            category_labels = {
                'data_request': 'Data Request',
                'general': 'General Feedback',
                'map_issue': 'Map Issue',
                'bug_report': 'Bug Report',
            }
            cat_label = category_labels.get(category, category)

            subject = f'[CCDA GeoPortal Feedback] {cat_label} from {name}'
            body = f"""
New feedback received on CCDA GeoPortal
========================================

Category:   {cat_label}
Name:       {name}
Email:      {email or 'Not provided'}
Submitted:  {fb.submitted_at.strftime('%Y-%m-%d %H:%M UTC')}
IP Address: {ip}

Message:
--------
{message}

========================================
View all feedback: http://192.168.2.16/admin/my_geonode/feedback/
            """

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@ccda.gov.pg'),
                    recipient_list=[r.strip() for r in os.environ.get('FEEDBACK_RECIPIENTS', 'victor.asipali@ccda.gov.pg').split(',')],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Email failure shouldn't block form submission

            # Slack notification
            try:
                import requests as req
                slack_webhook = os.environ.get('SLACK_WEBHOOK_URL', '')
                if not slack_webhook: raise ValueError('No Slack webhook configured')
                slack_msg = {
                    "blocks": [
                        {
                            "type": "header",
                            "text": {"type": "plain_text", "text": f"New {cat_label} - CCDA GeoPortal"}
                        },
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*Name:*\n{name}"},
                                {"type": "mrkdwn", "text": f"*Category:*\n{cat_label}"},
                                {"type": "mrkdwn", "text": f"*Email:*\n{email or 'Not provided'}"},
                                {"type": "mrkdwn", "text": f"*Submitted:*\n{fb.submitted_at.strftime('%Y-%m-%d %H:%M UTC')}"}
                            ]
                        },
                        {
                            "type": "section",
                            "text": {"type": "mrkdwn", "text": f"*Message:*\n{message}"}
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {"type": "plain_text", "text": "View in Admin"},
                                    "url": "http://192.168.2.16/admin/my_geonode/feedback/",
                                    "style": "primary"
                                }
                            ]
                        }
                    ]
                }
                req.post(slack_webhook, json=slack_msg, timeout=5)
            except Exception:
                pass  # Slack failure shouldn't block form submission

            success = True

    return render(request, 'feedback/feedback.html', {
        'success': success,
        'error': error,
        'page_title': 'Feedback',
    })
