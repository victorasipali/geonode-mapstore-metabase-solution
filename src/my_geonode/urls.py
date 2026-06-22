# -*- coding: utf-8 -*-
from django.urls import path
from geonode.urls import urlpatterns
from . import views

urlpatterns = [
    path('analytics/', views.analytics_dashboard, name='analytics-dashboard'),
    path('themes/', views.themes_catalogue, name='themes-catalogue'),
] + urlpatterns
