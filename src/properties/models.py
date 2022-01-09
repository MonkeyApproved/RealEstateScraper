from django.db import models
from django.utils import timezone


class Owner(models.Model):
    owner_email = models.CharField(max_length=100, primary_key=True)


class PageMetrics(models.Model):
    saves = models.IntegerField()
    visits = models.IntegerField()


class GeoLocation(models.Model):
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)


class XeProperty(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    created_on = models.DateTimeField(default=timezone.now)
    price_total = models.IntegerField()
    price_sqm = models.IntegerField()
    size_sqm = models.DecimalField(max_digits=10, decimal_places=1)
    construction_year = models.IntegerField(null=True)
    description = models.TextField(null=True)
    bathrooms = models.CharField(max_length=100, null=True)
    bedrooms = models.CharField(max_length=100, null=True)
    condition = models.CharField(max_length=100, null=True)
    furnished = models.BooleanField(null=True)
    renovated = models.BooleanField(null=True)
    item_type = models.CharField(max_length=100, null=True)
    property_type = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    location = models.ForeignKey(GeoLocation, on_delete=models.CASCADE)
    metrics = models.ForeignKey(PageMetrics, on_delete=models.CASCADE)
