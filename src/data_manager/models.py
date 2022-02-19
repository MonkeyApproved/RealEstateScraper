from django.db import models


class LoadConfiguration(models.Model):
    frequency = models.IntegerField()
    transaction_name = models.CharField(max_length=20)
    item_type = models.CharField(max_length=20)
    geo_place_id = models.CharField(max_length=50)
    maximum_price = models.IntegerField()
    minimum_construction_year = models.IntegerField()
    minimum_size = models.IntegerField()


class DataLoad(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=1000)
    count_total = models.IntegerField()
    count_new = models.IntegerField()
    load_config = models.ForeignKey(LoadConfiguration, on_delete=models.CASCADE)
