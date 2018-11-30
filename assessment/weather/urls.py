from django.urls import path
from . import views

urlpatterns = [
    path('weather/<lat>/<lon>/', views.weather),
    path('weather/<lat>/<lon>/<site_1>/', views.weather),
    path('weather/<lat>/<lon>/<site_1>/<site_2>/', views.weather),
]
