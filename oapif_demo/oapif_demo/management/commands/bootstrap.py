import os

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand
from oapif_demo.models import Apiary, Area, PollenConsumption, Review, Track


class Command(BaseCommand):
    help = "Reset and setup project."

    def handle(self, *args, **options):

        call_command("migrate", "--no-input")
        call_command("flush", "--no-input")
        call_command("createsuperuser", "--no-input")
        call_command("loaddata", "data.json")

        readwrite_user = User.objects.create_user(
            username=os.getenv("DJANGO_READWRITE_USER_USERNAME"),
            password=os.getenv("DJANGO_READWRITE_USER_PASSWORD"),
            is_staff=True,
        )
        readonly_user = User.objects.create_user(
            username=os.getenv("DJANGO_READONLY_USER_USERNAME"),
            password=os.getenv("DJANGO_READONLY_USER_PASSWORD"),
            is_staff=True,
        )
        for model in [Apiary, Area, Track, Review, PollenConsumption]:
            ct = ContentType.objects.get_for_model(model)
            read_perm = Permission.objects.get(
                content_type=ct, codename=f"view_{model._meta.model_name}"
            )
            add_perm = Permission.objects.get(
                content_type=ct, codename=f"add_{model._meta.model_name}"
            )
            del_perm = Permission.objects.get(
                content_type=ct, codename=f"delete_{model._meta.model_name}"
            )
            change_perm = Permission.objects.get(
                content_type=ct, codename=f"change_{model._meta.model_name}"
            )

            readonly_user.user_permissions.add(read_perm)
            readwrite_user.user_permissions.add(
                read_perm, add_perm, del_perm, change_perm
            )

        readonly_user.save()
