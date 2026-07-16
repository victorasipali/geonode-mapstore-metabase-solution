
## GeoServer Memory
GeoServer requires at least 2GB heap for 80+ layers.
In .env file: `-Xms512M -Xmx2048M`
Default was 768M which caused 504 timeouts.
