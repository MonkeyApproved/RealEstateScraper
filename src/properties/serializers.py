from rest_framework import serializers
from .models import XeResult, XeResidence, GeoLocation, PageMetrics, Owner


class XeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeResult
        fields = '__all__'


class XeResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = XeResidence
        fields = '__all__'


class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = '__all__'


class PageMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageMetrics
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'
