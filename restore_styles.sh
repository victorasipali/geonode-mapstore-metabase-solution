#!/bin/bash
# Restore critical GeoServer SLD styles after restart
echo "Restoring GeoServer styles..."

GS="http://192.168.2.16/geoserver/rest"
AUTH="admin:geoserver"
SLD_DIR="/opt/geonode-project/my_geonode/src/my_geonode/static/sld"

for sld in $SLD_DIR/*.sld; do
  name=$(basename "${sld%.sld}")
  echo "Uploading: $name"
  # Try POST first, if fails use PUT (style exists)
  result=$(curl -s -o /dev/null -w "%{http_code}" -u $AUTH \
    -X POST -H "Content-Type: application/vnd.ogc.sld+xml" \
    -d @"$sld" \
    "$GS/styles?name=$name")
  if [ "$result" = "403" ]; then
    curl -s -u $AUTH \
      -X PUT -H "Content-Type: application/vnd.ogc.sld+xml" \
      -d @"$sld" \
      "$GS/styles/$name"
    echo "  Updated: $name"
  else
    echo "  Created: $name ($result)"
  fi
done

# Apply province style to province layer
curl -s -u $AUTH \
  -X PUT -H "Content-Type: application/json" \
  -d '{"layer":{"defaultStyle":{"name":"png_provinces"}}}' \
  "$GS/layers/geonode:gadm41_PNG_1"

curl -s -u $AUTH -X POST "$GS/reload"
echo "Styles restored!"

# Restore GeoFence rules for all datasets
echo "Restoring GeoFence rules..."
docker exec django4my_geonode python3 -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_geonode.settings')
django.setup()
from geonode.geoserver.security import gf_utils, invalidate_geofence_cache
from geonode.geoserver.geofence import Rule
from geonode.layers.models import Dataset
geofence = gf_utils.geofence
all_rules = geofence.get_rules()
existing = {r.get('layer') for r in all_rules['rules'] if r.get('layer')}
priority = gf_utils.get_first_available_priority()
added = 0
for d in Dataset.objects.all():
    if d.name not in existing:
        try:
            rule = Rule(access='ALLOW', priority=priority, workspace='geonode', layer=d.name)
            geofence.insert_rule(rule)
            priority += 1
            added += 1
        except: pass
if added > 0:
    invalidate_geofence_cache()
print(f'GeoFence: {added} rules restored')
" 2>/dev/null

# Restore Metabase nginx proxy config
echo "Restoring Metabase nginx config..."
docker exec nginx4my_geonode sh -c 'cat > /etc/nginx/sites-enabled/metabase.conf << "NGINXEOF"
location /metabase/ {
    proxy_pass http://metabase4my_geonode:3000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 300;
    client_max_body_size 100M;
}

location = /metabase {
    return 302 /metabase/;
}
NGINXEOF'
docker exec nginx4my_geonode nginx -s reload
echo "Metabase nginx config restored!"

# Restore nginx WMS cache config
echo "Restoring nginx WMS cache..."
docker exec nginx4my_geonode sh -c 'grep -q "proxy_cache_path" /etc/nginx/nginx.conf || sed -i "s|resolver 127.0.0.11;|resolver 127.0.0.11;\n    proxy_cache_path /tmp/nginx_wms_cache levels=1:2 keys_zone=wms_cache:10m max_size=500m inactive=60m use_temp_path=off;|" /etc/nginx/nginx.conf'
docker exec nginx4my_geonode sh -c 'cat > /etc/nginx/sites-enabled/wms_cache.conf << "NGINXEOF"
location /geoserver/ows {
    proxy_cache wms_cache;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 1h;
    proxy_cache_valid 404 1m;
    proxy_cache_bypass $http_pragma;
    proxy_cache_use_stale error timeout updating;
    proxy_ignore_headers Cache-Control;
    add_header X-Cache-Status $upstream_cache_status;
    proxy_pass http://geoserver:8080/geoserver/ows;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 120;
    client_max_body_size 10M;
}
NGINXEOF'
docker exec nginx4my_geonode nginx -s reload
echo "WMS cache restored!"
