# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, AddUsersToGroupForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, admin_user

@unauthenticated_user
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

@unauthenticated_user
def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'profile.html')

@login_required(login_url='/login/') # only allow admins to do this
@admin_user
def add_users_to_group(request):
    template = 'manage_user_roles.html'
    msg = None

    if request.method == "POST":
        form = AddUsersToGroupForm(request.POST)

        if form.is_valid():
            group = form.cleaned_data['all_groups']
            users = [User.objects.get(pk=pk) for pk in request.POST.getlist('all_users', '')]
            for user in users:
                user.groups.clear()
                user.groups.add(group)

            msg = "User roles successfully updated!"
            # return redirect('dashboard')
            
    else:
        form = AddUsersToGroupForm()

    return render(request, template, {"form" : form, "msg": msg, "users": User.objects.all()})

@login_required(login_url='/login/')
def update_profile(request):
    template = 'profile.html'
    msg = None

    if request.method == "POST":
        form = UpdateProfileForm(request.POST)

        if form.is_valid():

            user = request.user
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.email = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()
    
            msg = "User sucessfully updated!"
    else:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
        form = UpdateProfileForm(initial={'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name})
    
    return render(request, template, {"form" : form, "msg": msg,})