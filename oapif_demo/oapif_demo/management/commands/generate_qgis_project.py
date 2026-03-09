import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate the QGIS project based on server configuration"

    def handle(self, *args, **options):
        dev_qgs = Path(f"{settings.STATIC_ROOT}/qgis/bees_dev.qgs").read_text()
        qgs = dev_qgs.replace(
            "https://localhost",
            f"https://{os.getenv('CADDY_DOMAIN')}",
        )
        Path(f"{settings.STATIC_ROOT}/qgis/bees.qgs").write_text(qgs)
