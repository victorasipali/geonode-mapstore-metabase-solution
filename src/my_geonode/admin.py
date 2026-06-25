from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .feedback import Feedback
import os


def mark_reviewed(modeladmin, request, queryset):
    queryset.update(status='reviewed')
    messages.success(request, f'{queryset.count()} feedback(s) marked as Reviewed.')
mark_reviewed.short_description = 'Mark selected as Reviewed'


def mark_resolved(modeladmin, request, queryset):
    import requests as req
    slack_webhook = os.environ.get('SLACK_WEBHOOK_URL', '')
    for fb in queryset:
        fb.status = 'resolved'
        fb.resolved_at = timezone.now()
        fb.resolved_by = request.user.username
        fb.save()
        # Notify Slack
        if slack_webhook:
            try:
                req.post(slack_webhook, json={
                    "blocks": [
                        {
                            "type": "header",
                            "text": {"type": "plain_text", "text": f"✅ Resolved: {fb.get_category_display()}"}
                        },
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*From:*\n{fb.name}"},
                                {"type": "mrkdwn", "text": f"*Resolved by:*\n{request.user.username}"},
                                {"type": "mrkdwn", "text": f"*Original message:*\n{fb.message[:200]}"},
                                {"type": "mrkdwn", "text": f"*Admin notes:*\n{fb.admin_notes or 'None'}"},
                            ]
                        }
                    ]
                }, timeout=5)
            except Exception:
                pass
    messages.success(request, f'{queryset.count()} feedback(s) marked as Resolved and Slack notified.')
mark_resolved.short_description = 'Mark selected as Resolved + notify Slack'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'category', 'status', 'submitted_at', 'resolved_by']
    list_filter = ['category', 'status', 'submitted_at']
    search_fields = ['name', 'email', 'message', 'admin_notes']
    readonly_fields = ['submitted_at', 'ip_address', 'resolved_at']
    ordering = ['-submitted_at']
    list_per_page = 25
    actions = [mark_reviewed, mark_resolved]
    fieldsets = (
        ('Submission', {
            'fields': ('name', 'email', 'category', 'message', 'submitted_at', 'ip_address')
        }),
        ('Admin Response', {
            'fields': ('status', 'admin_notes', 'resolved_by', 'resolved_at'),
            'classes': ('wide',)
        }),
    )
