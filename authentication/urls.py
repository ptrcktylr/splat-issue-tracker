# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, profile_view, register_user, add_users_to_group, update_profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', update_profile, name="profile"),
    path('role-managment/', add_users_to_group, name="role-managment")
]
