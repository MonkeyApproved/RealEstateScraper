from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

from . import views
from scraping.xe import PropertyType, Xe

router = DefaultRouter()
router.register(r'load_config', views.LoadConfigView)
router.register(r'data_loads', views.DataLoadView)


urlpatterns = [
    path("", include(router.urls)),
]
