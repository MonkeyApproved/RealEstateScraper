from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models



class XeResultView(ModelViewSet):
    serializer_class = serializers.XeResultSerializer
    queryset = models.XeResult.objects.all()


class OwnerView(ModelViewSet):
    serializer_class = serializers.OwnerSerializer
    queryset = models.Owner.objects.all()


class XeResidenceList(ModelViewSet):
    queryset = models.XeResidence.objects.all()
    serializer_class = serializers.XeResidence


class XeResidenceDetail(ModelViewSet):
    queryset = models.XeResidence.objects.all()
    serializer_class = serializers.XeResidence


class XeResidenceView(ModelViewSet):
    serializer_class = serializers.XeResidence
    queryset = models.XeResidence.objects.all()


class GeoLocationView(ModelViewSet):
    serializer_class = serializers.GeoLocationSerializer
    queryset = models.GeoLocation.objects.all()


class PageMetricsView(ModelViewSet):
    serializer_class = serializers.PageMetrics
    queryset = models.PageMetrics.objects.all()
