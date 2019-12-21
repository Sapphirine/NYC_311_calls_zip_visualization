from django.urls import path, include
from . import views
# '' represents root of the project
# i.e. /maphousing
urlpatterns = [
    path('', views.home),
]
