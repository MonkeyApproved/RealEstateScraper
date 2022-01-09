from django.urls import path
from . import views

urlpatterns = [
    path("help/", views.help),
    path("igmo/", views.igmo),
    path("scrape_now/", views.scrape_now),
]
