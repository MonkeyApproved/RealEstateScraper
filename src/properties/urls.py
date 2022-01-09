from django.urls import path
from . import views

urlpatterns = [
    path("", views.igmo),
    path("help/", views.help),
    path("igmo/", views.igmo),
    path("scrape_now/", views.scrape_now),
]
