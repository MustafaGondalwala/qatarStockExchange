from django.urls import path

from . import views

urlpatterns = [
    path('realtime-data', views.getData, name='getData'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
]
