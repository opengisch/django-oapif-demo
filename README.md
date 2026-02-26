# Django OAPIF demo project

1. Start and bootstrap the project:

```bash
cp .example.env .env
docker compose --build up -d
docker compose exec django python manage.py bootstrap
```


2. Open QGIS
3. Import `qgis/auth.xml` in Settings > Options > Authentication > Utilities > Import Authentication Configurations from File 
4. Open project `qgis/bees.qgz`
