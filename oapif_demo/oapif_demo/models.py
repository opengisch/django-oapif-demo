import uuid

from django.contrib.gis.db import models


class Apiary(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nbr_of_boxes = models.IntegerField()
    bee_species = models.TextField()
    bee_amount = models.TextField()
    beekeeper = models.TextField()
    picture = models.TextField()
    disease = models.IntegerField()
    kind_of_disease = models.TextField(null=True)
    average_harvest = models.IntegerField(null=True)
    area = models.ForeignKey("Area", null=True, on_delete=models.SET_NULL)
    source = models.TextField(null=True)
    quality = models.TextField(null=True)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)
    horizontal_accuracy = models.FloatField(null=True)
    nr_used_satellites = models.IntegerField(null=True)
    fix_status_descr = models.TextField(null=True)
    position_locked = models.BooleanField(null=True)
    geom = models.PointField(srid=4326)


class Area(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proprietor = models.TextField()
    plant_species = models.TextField()
    picture = models.TextField()
    review_date = models.DateField()
    reviewer = models.TextField()
    geom = models.PolygonField(srid=4326)


class Tracks(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    region = models.TextField()
    editor = models.TextField()
    geom = models.LineStringField(srid=4326)


class Reviews(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.TextField()
    review_date = models.DateField()
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE)


class PollenConsumption(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percentage = models.IntegerField()
    apiary = models.ForeignKey(Apiary, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
