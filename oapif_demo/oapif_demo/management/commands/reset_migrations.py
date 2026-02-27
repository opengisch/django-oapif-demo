from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete all migrations for oapif_demo and re-run makemigrations + migrate"

    def handle(self, *args, **options):
        app_name = "oapif_demo"
        migrations_path = Path(app_name) / "migrations"

        call_command("migrate", "oapif_demo", "zero")

        self.stdout.write("Deleting migration files...")
        for file in migrations_path.glob("*.py"):
            if file.name != "__init__.py":
                file.unlink()

        self.stdout.write("Running makemigrations...")
        call_command("makemigrations", app_name)
        self.stdout.write("Running migrate...")
        call_command("migrate")
        self.stdout.write(self.style.SUCCESS("Migrations reset successfully."))
