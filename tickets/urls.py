# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='tickets'),
    path('ticket/', views.ticket, name='ticket-num'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/new/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/update', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/adminupdate', views.TicketAdminUpdateView.as_view(), name='ticket-admin-update'),
    path('ticket/<int:pk>/devupdate', views.TicketDeveloperUpdateView.as_view(), name='ticket-developer-update'),
    path('ticket/<int:pk>/comment/new', views.CommentCreateView.as_view(), name='comment-create'),
    path('ticket/<int:pk>/attachment/new', views.AttachmentCreateView.as_view(), name='attachment-create'),
]
