# Django OAPIF demo project

1. Start and bootstrap the project:

```bash
cp .example.env .env
docker compose up --build -d
```

2. Open QGIS
3. Import `oapif_demo/static/qgis/auth.xml` in Settings > Options > Authentication > Utilities > Import Authentication Configurations from File 
4. Open project `oapif_demo/static/qgis/bees_dev.qgs`
