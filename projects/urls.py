# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update', views.ProjectUpdateView.as_view(), name='project-update'),
]
