from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.index, name='index'),
    path('statistics', views.statistics, name='statistics'),
    path('track_analysis', views.track_analysis, name='track_analysis')
]
