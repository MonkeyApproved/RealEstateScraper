from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

from . import views
from scraping.xe import PropertyType, Xe

router = DefaultRouter()
router.register(r'load_config', views.LoadConfigView)
router.register(r'data_loads', views.DataLoadView)


def scrape_now(request):
    xe = Xe(
        type=PropertyType.RESIDENCE,
        max_price=150000,
        min_size=90,
        min_year=2000,
    )
    count = xe.check_for_properties(
        save_details_to_disc=False, save_images=False, save_to_db=True
    )
    return HttpResponse(f"Parsed a total of {count} properties.")


urlpatterns = [
    path("", include(router.urls)),
]
