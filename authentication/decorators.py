from django.http import HttpRequest
from django.shortcuts import redirect

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_function(request, *args, **kwargs)
    
    return wrapper_function

def admin_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return view_function(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_function

def project_manager_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name='project manager').exists() or request.user.groups.filter(name='admin').exists():
            return view_function(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_function

def developer_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name='developer').exists() or request.user.groups.filter(name='admin').exists():
            return view_function(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_function

def submitter_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.filter(name='submitter').exists() or request.user.groups.filter(name='admin').exists():
            return view_function(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_function