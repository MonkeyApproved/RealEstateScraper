from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import LoadConfiguration, DataLoad


class LoadConfigurationSerializer(ModelSerializer):
    class Meta:
        model = LoadConfiguration
        fields = '__all__'


class DataLoadSerializer(ModelSerializer):
    load_config = LoadConfigurationSerializer()
    class Meta:
        model = DataLoad
        fields = '__all__'
