from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from leaflet.admin import LeafletGeoAdminMixin
from unfold.admin import ModelAdmin as BaseModelAdmin
from unfold.admin import TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from oapif_demo.models import (
    Apiary,
    Area,
    PollenConsumption,
    Review,
    Track,
)

admin.site.unregister(User)
admin.site.unregister(Group)


class ModelAdmin(LeafletGeoAdminMixin, BaseModelAdmin): ...


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class ReviewAdminInline(TabularInline):
    model = Review
    exclude = ["uuid"]
    extra = 0
    tab = True
    hide_title = True


class PollenConsumptionAdminInline(TabularInline):
    model = PollenConsumption
    exclude = ["uuid"]
    extra = 0
    tab = True
    hide_title = True


@admin.register(Apiary)
class ApiaryAdmin(ModelAdmin):
    inlines = (
        ReviewAdminInline,
        PollenConsumptionAdminInline,
    )
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "geom",
                    "nbr_of_boxes",
                    "bee_species",
                    "beekeeper",
                    "average_harvest",
                ],
            },
        ),
        (
            "Picture",
            {
                "fields": [
                    "picture",
                ],
            },
        ),
        (
            "Issues",
            {
                "fields": [
                    "disease",
                    "kind_of_disease",
                ],
            },
        ),
        (
            "GNSS",
            {
                "fields": [
                    "source",
                    "quality",
                    "x",
                    "y",
                    "z",
                    "horizontal_accuracy",
                    "nr_used_satellites",
                    "fix_status_descr",
                    "position_locked",
                ],
            },
        ),
    )


@admin.register(Area)
class AreaAdmin(ModelAdmin):
    inlines = (PollenConsumptionAdminInline,)
    fields = (
        "geom",
        "proprietor",
        "plant_species",
        "picture",
        "review_date",
        "reviewer",
    )


@admin.register(Track)
class TracksAdmin(ModelAdmin):
    fields = (
        "geom",
        "name",
        "region",
        "editor",
    )
