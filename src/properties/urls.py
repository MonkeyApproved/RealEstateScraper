from django.urls import path
from . import views

urlpatterns = [path("help/", views.help), path("igmo/", views.igmo)]
