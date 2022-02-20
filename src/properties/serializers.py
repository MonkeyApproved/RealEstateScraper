from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import XeResult, XeResidence, GeoLocation, PageMetrics, Owner


class XeResidenceSerializer(ModelSerializer):
    class Meta:
        model = XeResidence
        fields = '__all__'


class GeoLocationSerializer(ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = '__all__'


class PageMetricsSerializer(ModelSerializer):
    class Meta:
        model = PageMetrics
        fields = '__all__'


class OwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class XeResultSerializer(ModelSerializer):
    details = XeResidenceSerializer()
    location = GeoLocationSerializer()
    owner = SlugRelatedField(
        slug_field='email',
        read_only=True
    )
    class Meta:
        model = XeResult
        fields = '__all__'
