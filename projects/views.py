from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from .models import Project
from tickets.models import Ticket
from django.contrib.auth.models import User
from .forms import ProjectForm

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
    form_class = ProjectForm

    def form_valid(self, form):
        form.save()
        form.instance.assigned_users.add(self.request.user)
        return super().form_valid(form)

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)