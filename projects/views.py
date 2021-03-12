from django.shortcuts import render

def dashboard(request):
    return render(request, 'projects/dashboard.html')

def projects(request):
    return render(request, 'projects/projects.html')

def profile(request):
    return render(request, 'projects/profile.html')