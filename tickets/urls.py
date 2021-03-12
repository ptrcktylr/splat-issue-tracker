# -*- encoding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.tickets, name='tickets'),
    path('ticket/', views.ticket, name='ticket-num'),
]
