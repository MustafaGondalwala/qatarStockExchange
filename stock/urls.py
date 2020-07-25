from django.urls import path

from . import views

urlpatterns = [
    path('realtime-data', views.getData, name='getData'),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('volume',views.volume,name="volume"),
    path('all',views.all,name="volume"),
    path('mainpage',views.mainpage,name="volume"),
    path('currentprice',views.currentprice,name="volume"),
    path('report',views.report,name="one_day"),
    path('top10',views.top10,name="one_day"),

]
