#!/bin/bash
# Fix site domain after rebuild
echo "Fixing site domain..."
docker exec django4my_geonode python3 -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_geonode.settings')
django.setup()
from django.contrib.sites.models import Site
site = Site.objects.get_or_create(id=1)[0]
site.domain = '192.168.2.16'
site.name = 'CCDA GeoPortal'
site.save()
print('Site domain fixed:', site.domain)
"
echo "Done"
