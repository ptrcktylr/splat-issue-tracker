from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Project
from tickets.models import Ticket
from django.contrib.auth.models import User

def dashboard(request):
    return render(request, 'projects/dashboard.html')

def projects(request):
    context = {
        'projects': Project.objects.all(),
        }
    return render(request, 'projects/projects.html', context)

def profile(request):
    return render(request, 'projects/profile.html')

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'projects'
    ordering = ['-created_at']

class ProjectDetailView(DetailView):
    model = Project

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'description', 'assigned_users']