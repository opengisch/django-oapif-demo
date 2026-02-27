import uuid

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Apiary(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nbr_of_boxes = models.IntegerField(verbose_name="Number of Boxes")
    bee_species = models.CharField(max_length=None, verbose_name="Species of Bees")
    bee_amount = models.CharField(max_length=None, verbose_name="Amount of Bees")
    beekeeper = models.CharField(max_length=None, verbose_name="Beekeeper")
    picture = models.CharField(max_length=None, verbose_name="Photo")
    disease = models.BooleanField(verbose_name="Infected")
    kind_of_disease = models.CharField(max_length=None, null=True, blank=True)
    average_harvest = models.IntegerField(null=True, verbose_name="Yearly Harvest (kg)")
    area = models.ForeignKey("Area", null=True, on_delete=models.SET_NULL)
    source = models.CharField(max_length=None, null=True, blank=True)
    quality = models.CharField(max_length=None, null=True, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    z = models.FloatField(null=True, blank=True)
    horizontal_accuracy = models.FloatField(null=True, blank=True)
    nr_used_satellites = models.IntegerField(null=True, blank=True)
    fix_status_descr = models.CharField(max_length=None, null=True, blank=True)
    position_locked = models.BooleanField(null=True, blank=True)
    geom = models.PointField(srid=4326)

    def __str__(self):
        return f"{self.bee_species} ({self.nbr_of_boxes} boxes, {self.beekeeper})"


class Area(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proprietor = models.CharField(max_length=None)
    plant_species = models.CharField(max_length=None)
    picture = models.CharField(max_length=None)
    review_date = models.DateField()
    reviewer = models.CharField(max_length=None)
    geom = models.PolygonField(srid=4326)

    def __str__(self):
        return f"{self.uuid} - {self.plant_species} ({self.proprietor})"


class Track(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=None)
    region = models.CharField(max_length=None)
    editor = models.CharField(max_length=None)
    geom = models.LineStringField(srid=4326)


class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.CharField(max_length=None)
    review_date = models.DateField()
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE, related_name="review")


class PollenConsumption(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percentage = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE)
    area = models.ForeignKey(
        Area, null=True, on_delete=models.CASCADE, related_name="pollen_consumption"
    )
