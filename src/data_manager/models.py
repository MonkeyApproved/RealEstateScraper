from django.db import models
from django.utils import timezone


class LoadConfiguration(models.Model):
    config_name = models.CharField(max_length=100)
    frequency = models.IntegerField()
    item_type = models.CharField(max_length=20)
    geo_place_id = models.CharField(max_length=50)
    maximum_price = models.IntegerField(null=True)
    minimum_construction_year = models.IntegerField(null=True)
    minimum_size = models.IntegerField(null=True)


class DataLoad(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=1000)
    count_total = models.IntegerField()
    count_new = models.IntegerField()
    completed = models.BooleanField()
    load_config = models.ForeignKey(LoadConfiguration, on_delete=models.CASCADE)
