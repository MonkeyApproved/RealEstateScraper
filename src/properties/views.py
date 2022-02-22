from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter

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

class XeResultFilter(filters.FilterSet):
    min_bathrooms = filters.NumberFilter(field_name="details__bathrooms", lookup_expr='gte')
    min_bedrooms = filters.NumberFilter(field_name="details__bedrooms", lookup_expr='gte')
    area = filters.CharFilter(field_name="details__area", lookup_expr='exact')
    price = filters.NumberFilter(field_name="details__price_total", lookup_expr='exact')
    min_price = filters.NumberFilter(field_name="details__price_total", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="details__price_total", lookup_expr='lte')

    class Meta:
        model = models.XeResult
        fields = ['id', 'xe_id', 'last_parsed_on']


class XeResultView(ModelViewSet, ListAPIView):
    serializer_class = serializers.XeResultSerializer
    queryset = models.XeResult.objects.all()
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = XeResultFilter
    ordering_fields = ['last_parsed_on', 'xe_id']


class OwnerView(ModelViewSet, ListAPIView):
    serializer_class = serializers.OwnerSerializer
    queryset = models.Owner.objects.all()


class XeResidenceList(ModelViewSet, ListAPIView):
    queryset = models.XeResidence.objects.all()
    serializer_class = serializers.XeResidence


class XeResidenceDetail(ModelViewSet, ListAPIView):
    queryset = models.XeResidence.objects.all()
    serializer_class = serializers.XeResidence


class XeResidenceView(ModelViewSet, ListAPIView):
    serializer_class = serializers.XeResidence
    queryset = models.XeResidence.objects.all()


class GeoLocationView(ModelViewSet, ListAPIView):
    serializer_class = serializers.GeoLocationSerializer
    queryset = models.GeoLocation.objects.all()


class PageMetricsView(ModelViewSet, ListAPIView):
    serializer_class = serializers.PageMetrics
    queryset = models.PageMetrics.objects.all()
