"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from properties import views

router = routers.DefaultRouter()
router.register(r'xe_result', views.XeResultView)
router.register(r'xe_residence', views.XeResidenceView)
router.register(r'xe_owner', views.OwnerView)
router.register(r'geo_location', views.GeoLocationView)
router.register(r'page_metrics', views.PageMetricsView)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path("properties/", include("properties.urls")),
]
