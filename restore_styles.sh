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
