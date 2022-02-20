from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models


class LoadConfigView(ModelViewSet):
    serializer_class = serializers.LoadConfigurationSerializer
    queryset = models.LoadConfiguration.objects.all()


class DataLoadView(ModelViewSet):
    serializer_class = serializers.DataLoadSerializer
    queryset = models.DataLoad.objects.all()
