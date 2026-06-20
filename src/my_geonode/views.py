from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .metabase import get_metabase_embed_url


@login_required
def analytics_dashboard(request):
    """
    Renders the Metabase GeoNode Overview dashboard (ID: 2)
    embedded inside a GeoNode page via signed JWT iframe.
    """
    metabase_url = get_metabase_embed_url(
        dashboard_id=2,
        bordered=False,
        titled=False
    )
    return render(request, 'metabase/dashboard.html', {
        'metabase_url': metabase_url,
        'page_title': 'Analytics Dashboard'
    })
