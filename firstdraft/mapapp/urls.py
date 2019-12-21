from django.conf.urls import url
from . import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^map/', views.mapper),
    url(r'^form/', views.form),
    url(r'^$', views.frontpage),
]