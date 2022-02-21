from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models


def detailsView(request, xe_id: str):
    xe_results = models.XeResult.objects.filter(xe_id=xe_id)
    details = [model_to_dict(result.details) for result in xe_results]
    geo = [model_to_dict(result.location) for result in xe_results]
    owner = [model_to_dict(result.owner) for result in xe_results]
    metrics = models.PageMetrics.objects.filter(xe_id=xe_id)
    return JsonResponse({
        'xe_result': list(xe_results.values()),
        'details': details,
        'location': geo,
        'owner': owner,
        'metrics': list(metrics.values()),
    })


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
