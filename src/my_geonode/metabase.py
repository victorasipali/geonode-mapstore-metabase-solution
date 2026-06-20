import jwt
import time
from django.conf import settings


def get_metabase_embed_url(dashboard_id, params=None, bordered=True, titled=True):
    """
    Generate a signed Metabase embed URL for the given dashboard ID.
    Requires METABASE_SITE_URL and METABASE_SECRET_KEY in settings.py
    """
    if params is None:
        params = {}

    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": params,
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiry
    }

    token = jwt.encode(
        payload,
        settings.METABASE_SECRET_KEY,
        algorithm="HS256"
    )

    options = f"bordered={'true' if bordered else 'false'}&titled={'true' if titled else 'false'}"
    return f"{settings.METABASE_SITE_URL}/embed/dashboard/{token}#{options}"
