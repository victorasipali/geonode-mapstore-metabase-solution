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
