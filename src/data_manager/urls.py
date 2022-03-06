from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'load_config', views.LoadConfigView)
router.register(r'data_loads', views.DataLoadView)


urlpatterns = [
    path("", include(router.urls)),
    path("trigger_load/<int:load_id>/", views.trigger_load)
]
