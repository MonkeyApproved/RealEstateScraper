from django.db import models
from django.utils import timezone


class Owner(models.Model):
    account_id = models.IntegerField()
    email = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    ref_id = models.CharField(max_length=100, null=True)
    company_title = models.CharField(max_length=100, null=True)
    active_ads = models.IntegerField(null=True)


class PageMetrics(models.Model):
    date = models.DateTimeField(default=timezone.now)
    xe_id = models.IntegerField()
    saves = models.IntegerField()
    visits = models.IntegerField()


class GeoLocation(models.Model):
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)


class XeResidence(models.Model):
    price_total = models.IntegerField()
    price_sqm = models.IntegerField()
    size_sqm = models.DecimalField(max_digits=10, decimal_places=1)
    construction_year = models.IntegerField(null=True)
    area = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    bathrooms = models.CharField(max_length=100, null=True)
    bedrooms = models.CharField(max_length=100, null=True)
    commercial = models.BooleanField(null=True)
    item_type = models.CharField(max_length=100, null=True)
    property_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'property in {self.area} for {self.price_total}'


class XeResult(models.Model):
    xe_id = models.IntegerField()
    first_parsed_on = models.DateTimeField(default=timezone.now)
    last_parsed_on = models.DateTimeField(default=timezone.now)
    created = models.DateField(null=True)
    modified = models.DateField(null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    location = models.ForeignKey(GeoLocation, on_delete=models.CASCADE)
    details = models.ForeignKey(XeResidence, on_delete=models.CASCADE)
