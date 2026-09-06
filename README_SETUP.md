# CCDA GeoPortal — Post-Restart Checklist

## After every restart:
cd /opt/geonode-project/my_geonode
docker compose up -d
docker compose -f docker-compose.metabase.yml start
sleep 40
./fix_site_domain.sh
./restore_styles.sh

## URLs:
- Portal: http://192.168.2.16/
- Themes: http://192.168.2.16/themes/
- Analytics: http://192.168.2.16/analytics/
- Metabase: http://192.168.2.16/metabase/
- GeoServer: http://192.168.2.16/geoserver/web/

## Credentials:
- GeoNode admin: admin / admin
- GeoServer: admin / geoserver
- Metabase: victor.asipali@ccda.gov.pg / CCDA@dm1n#2026

## Notes:
- Nginx config (metabase proxy + WMS cache) is baked into the image
- No manual nginx patching needed after rebuild
- GWC tile cache at /opt/geoserver_data/gwc/
- SLD styles at src/my_geonode/static/sld/
