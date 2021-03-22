# -*- encoding: utf-8 -*-

from django.urls import path
from . import views
from tickets.views import TicketWithProjectCreateView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/ticket/new', TicketWithProjectCreateView.as_view(), name='project-ticket-create'),
    path('admin-project-managment/', views.admin_project_managment, name='admin-project-managment'),
    path('project-managment/', views.pm_project_managment, name='project-managment'),
    path('project-managment/<int:pk>/', views.pm_project_managment, name='single-project-managment'),
    path('admin-project-managment/<int:pk>/', views.admin_project_managment, name='single-admin-project-managment')
]
