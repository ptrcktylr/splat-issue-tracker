# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from re import template
from django.contrib import auth
from django.urls import path
from .views import login_view, profile_view, register_user, add_users_to_group, NewPasswordView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset/done/", 
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
        name="password_reset_done"),
    path("password-reset/", 
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
        name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
        name="password_reset_confirm"),
    path("password-reset-complete/", 
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
        name="password_reset_complete"),
    path('profile/', profile_view, name="profile"),
    path('role-managment/', add_users_to_group, name="role-managment"),
    path('new-password/', NewPasswordView.as_view(template_name='accounts/change_password.html'), name="new-password"),
]
