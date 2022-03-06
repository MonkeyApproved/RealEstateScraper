from data_manager.jobs.hourly.scrape import Job
from rest_framework.viewsets import ModelViewSet

from . import serializers
from . import models


def trigger_load(request, load_id: int = -1):
    if load_id == -1:
        return
    parser = Job()
    load_config = models.LoadConfiguration.objects.get(id=load_id)
    parser.run_collection(load_config=load_config)


class LoadConfigView(ModelViewSet):
    serializer_class = serializers.LoadConfigurationSerializer
    queryset = models.LoadConfiguration.objects.all()


class DataLoadView(ModelViewSet):
    serializer_class = serializers.DataLoadSerializer
    queryset = models.DataLoad.objects.all()
