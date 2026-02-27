import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import urlretrieve

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

FILE_URL = "https://github.com/opengisch/QField/raw/refs/heads/master/resources/sample_projects/datasets/bees.gpkg"

PG_CONN = (
    f"PG:host={os.environ['POSTGRES_HOST']} "
    f"port={os.environ['POSTGRES_PORT']} "
    f"dbname={os.environ['POSTGRES_DB']} "
    f"user={os.environ['POSTGRES_USER']} "
    f"password={os.environ['POSTGRES_PASSWORD']}"
)

LAYERS = [
    {
        "sql": "SELECT uuid, nbr_of_boxes, bee_species, bee_amount, beekeeper, picture, disease, kind_of_disease, average_harvest, source, quality, x, y, z, horizontal_accuracy, nr_used_satellites, fix_status_descr, position_locked, geom FROM apiary",
        "table": "apiary",
    },
    {
        "sql": "SELECT uuid, proprietor, plant_species, picture, review_date, reviewer, geom FROM area",
        "table": "area",
    },
    {
        "sql": "SELECT uuid, name, region, editor, geometry FROM tracks",
        "table": "track",
    },
    {
        "sql": "SELECT uuid, reviewer, review_date, CAST(apiary_uuid AS TEXT) AS apiary_id FROM reviews WHERE apiary_id != 60",
        "table": "review",
        "t_srs": None,
    },
    {
        "sql": "SELECT uuid, percentage, CAST(apiary_uuid AS TEXT) AS apiary_id, CAST(field_uuid AS TEXT) AS area_id FROM Pollen_Consumption",
        "table": "pollenconsumption",
        "t_srs": None,
    },
]


class Command(BaseCommand):
    help = "Delete all migrations for oapif_demo and re-run makemigrations + migrate"

    def handle(self, *args, **options):

        call_command("migrate", "--no-input")

        with transaction.atomic():
            for model in apps.get_app_config("oapif_demo").get_models():
                self.stdout.write(f"Clearing data from table '{model._meta.label}'...")
                model.objects.all().delete()

        tmp_dir = tempfile.TemporaryDirectory()
        file_path = Path(tmp_dir.name) / "bees.gpkg"

        print(f"Downloading {file_path}...")
        urlretrieve(FILE_URL, file_path)

        for layer in LAYERS:
            cmd = [
                "ogr2ogr",
                "-f",
                "PostgreSQL",
                PG_CONN,
                str(file_path),
                "-sql",
                layer["sql"],
                "-nln",
                f"oapif_demo_{layer['table']}",
                "-t_srs",
                "EPSG:4326",
                "-append",
                "-update",
            ]
            print(f"Importing {layer['table']}...")
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(e.stderr)
                sys.exit(e.returncode)

        fixture_dir = Path("oapif_demo/fixtures")
        fixture_dir.mkdir(exist_ok=True)
        fixture_path = fixture_dir / "data.json"

        self.stdout.write("Writing fixture...")
        with fixture_path.open("w") as f:
            call_command(
                "dumpdata",
                "oapif_demo",
                indent=2,
                stdout=f,
            )
