# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import notifications, NotificationDetailView

urlpatterns = [
    path('', notifications, name='notifications'),
    path('<int:pk>', NotificationDetailView.as_view(), name='notification')
]
