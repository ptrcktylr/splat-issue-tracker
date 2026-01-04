# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
    path("", include("authentication.urls")), # Auth routes - login / register
    # path("", include("app.urls")),             # UI Kits Html files
    path("", include("projects.urls")),
    path("", include("tickets.urls")),
    path("notifications/", include('notifications.urls')),
]

# Serve media files in production (Render uses whitenoise for static, but not media)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)