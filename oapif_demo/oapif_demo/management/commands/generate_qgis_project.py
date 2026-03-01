import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

SERVER_DOMAIN = os.getenv("CADDY_DOMAIN")
SERVER_PROTOCOL = "http" if settings.DEBUG else "https"


class Command(BaseCommand):
    help = "Generate the QGIS project based on server configuration"

    def handle(self, *args, **options):
        dev_qgs = Path(f"{settings.STATIC_ROOT}/qgis/bees_dev.qgs").read_text()
        qgs = dev_qgs.replace(
            "https://localhost/oapif",
            f"{SERVER_PROTOCOL}://{SERVER_DOMAIN}/oapif",
        )
        Path(f"{settings.STATIC_ROOT}/qgis/bees.qgs").write_text(qgs)
