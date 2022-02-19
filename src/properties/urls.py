from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'xe_result', views.XeResultView)
router.register(r'xe_residence', views.XeResidenceView)
router.register(r'xe_owner', views.OwnerView)
router.register(r'geo_location', views.GeoLocationView)
router.register(r'page_metrics', views.PageMetricsView)


urlpatterns = [
    path("", include(router.urls)),
]
