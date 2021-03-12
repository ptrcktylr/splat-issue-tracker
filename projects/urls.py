# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.projects, name='projects'),
    path('profile/', views.profile, name='profile'),
]
