import json
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
    from geonode.base.models import ResourceBase

    categories = []
    theme_data = {}

    for cat in GroupCategory.objects.all().order_by('name'):
        groups_data = []
        for g in cat.groups.all().order_by('title'):
            layers = ResourceBase.objects.filter(
                group=g.group, resource_type='dataset'
            ).order_by('title')
            layer_list = [
                {
                    'id': l.id,
                    'title': l.title,
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
