from tickets.models import Ticket
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='/login')
def dashboard(request):
   
    context = {
        'projects': Project.objects.all(),
        'Ticket': Ticket,
        'tickets':Ticket.objects.all(),
        'user_tickets':Ticket.objects.filter(assigned_to = request.user)
    }
    return render(request, 'projects/dashboard.html', context)

@login_required(login_url='/login')
def projects(request):
    context = {
        'projects': Project.objects.all(),
        }
    return render(request, 'projects/projects.html', context)

class ProjectListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Project
    template_name = 'projects/projects.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'projects'
    ordering = ['-created_at']

class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Project

class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.save()
        form.instance.assigned_users.add(self.request.user)
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)