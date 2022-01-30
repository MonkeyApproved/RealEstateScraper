from django.shortcuts import render
from django.http import HttpResponse
from scraping.xe import PropertyType, Xe
from rest_framework import viewsets
from . import serializers
from . import models


class XeResultView(viewsets.ModelViewSet):
    serializer_class = serializers.XeResultSerializer
    queryset = models.XeResult.objects.all()


class OwnerView(viewsets.ModelViewSet):
    serializer_class = serializers.OwnerSerializer
    queryset = models.Owner.objects.all()


class XeResidenceView(viewsets.ModelViewSet):
    serializer_class = serializers.XeResidence
    queryset = models.XeResidence.objects.all()


class GeoLocationView(viewsets.ModelViewSet):
    serializer_class = serializers.GeoLocationSerializer
    queryset = models.GeoLocation.objects.all()


class PageMetricsView(viewsets.ModelViewSet):
    serializer_class = serializers.PageMetrics
    queryset = models.PageMetrics.objects.all()


def help(request):
    return render(request, "help.html")


def igmo(request):
    return HttpResponse("Hi this is Igmo")


def scrape_now(request):
    xe = Xe(
        type=PropertyType.RESIDENCE,
        max_price=150000,
        min_size=90,
        min_year=2000,
    )
    count = xe.check_for_properties(
        save_details_to_disc=False, save_images=False, save_to_db=True
    )
    return HttpResponse(f"Parsed a total of {count} properties.")
