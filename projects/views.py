from django.http import request
from django.utils import decorators
from tickets.models import Ticket
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm, PMProjectManagmentForm, AdminProjectManagmentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from authentication.decorators import admin_user, developer_user, project_manager_user, submitter_user
from notifications.utilities import create_notification

@login_required(login_url='/login')
def dashboard(request):
   
    context = {
        'projects': Project.objects.all(),
        'Ticket': Ticket,
        'tickets':Ticket.objects.all(),
        'user_tickets':Ticket.objects.filter(assigned_to = request.user),
        'assigned_projects': request.user.assigned_projects.all(),
    }
    return render(request, 'projects/dashboard.html', context)

@login_required(login_url='/login')
def projects(request):
    return render(request, 'projects/projects.html')

class ProjectListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Project
    template_name = 'projects/projects.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'projects'

class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Project

decorators = [project_manager_user]
@method_decorator(decorators, name='dispatch')
class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        form.instance.assigned_users.add(self.request.user)
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def test_func(self):
        project = self.get_object()
        return (self.request.user == project.created_by) or (self.request.user.groups.filter(name='admin').exists())

@login_required(login_url='/login/') 
@admin_user # only allow admins to do this
def admin_project_managment(request):
    template = 'admin_project_managment.html'
    msg = None

    if request.method == 'POST':
        form = AdminProjectManagmentForm(request.POST)
        
        if form.is_valid():
            projects = [Project.objects.get(pk=pk) for pk in request.POST.getlist('projects', '')]
            admins = [User.objects.get(pk=pk) for pk in request.POST.getlist('admins', '')]
            project_managers = [User.objects.get(pk=pk) for pk in request.POST.getlist('project_managers', '')]
            developers = [User.objects.get(pk=pk) for pk in request.POST.getlist('developers', '')]
            submitters = [User.objects.get(pk=pk) for pk in request.POST.getlist('submitters', '')]

            for project in projects:
                # clear users
                if len(admins) + len(project_managers) + len(developers) + len(submitters) == 0 :
                    for dev in project.assigned_users.filter(groups__name='developer'):
                        create_notification(request, dev, f"You have been removed from project {project.name} by {request.user.get_full_name()}")
                    for sub in project.assigned_users.filter(groups__name='submitter'):
                        create_notification(request, sub, f"You have been removed from project {project.name} by {request.user.get_full_name()}")
                    for adm in project.assigned_users.filter(groups__name='admin'):
                        create_notification(request, adm, f"You have been removed from project {project.name} by {request.user.get_full_name()}")
                    for pm in project.assigned_users.filter(groups__name='project manager'):
                        create_notification(request, pm, f"You have been removed from project {project.name} by {request.user.get_full_name()}")
                    project.clear_admins()
                    project.clear_project_managers()
                    project.clear_developers()
                    project.clear_submitters()
                
                # assign users
                for admin in admins:
                    project.assigned_users.add(admin)
                    create_notification(request, admin, f"You have been added as an admin to project {project.name} by {request.user.get_full_name()}")
                for project_manager in project_managers:
                    project.assigned_users.add(project_manager)
                    create_notification(request, project_manager, f"You have been added as a project manager to project {project.name} by {request.user.get_full_name()}")
                for developer in developers:
                    project.assigned_users.add(developer)
                    create_notification(request, developer, f"You have been added as a developer to project {project.name} by {request.user.get_full_name()}")
                for submitter in submitters:
                    project.assigned_users.add(submitter)
                    create_notification(request, submitter, f"You have been added as submitter to project {project.name} by {request.user.get_full_name()}")

            msg = "Roles successfully assigned!"
    else:
        form = AdminProjectManagmentForm()
    
    return render(request, template, {"form":form, "msg":msg, "users": User.objects.all()})

@login_required(login_url='/login/') 
@project_manager_user # only allow PMs to do this
def pm_project_managment(request):
    template = 'pm_project_managment.html'
    msg = None

    if request.method == 'POST':
        form = PMProjectManagmentForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            projects = [Project.objects.get(pk=pk) for pk in request.POST.getlist('projects', '')]
            developers = [User.objects.get(pk=pk) for pk in request.POST.getlist('developers', '')]
            submitters = [User.objects.get(pk=pk) for pk in request.POST.getlist('submitters', '')]

            for project in projects:
                if len(developers) + len(submitters) == 0 :
                    for dev in project.assigned_users.filter(groups__name='developer'):
                        create_notification(request, dev, f"You have been removed from project {project.name} by {request.user.get_full_name()}")
                    for sub in project.assigned_users.filter(groups__name='submitter'):
                        create_notification(request, sub, f"You have been removed from project {project.name} by {request.user.get_full_name()}")
                    project.clear_developers()
                    project.clear_submitters()

                # assign users
                for developer in developers:
                    project.assigned_users.add(developer)
                    create_notification(request, developer, f"You have been added as a developer to project {project.name} by {request.user.get_full_name()}")
                for submitter in submitters:
                    project.assigned_users.add(submitter)
                    create_notification(request, submitter, f"You have been added as a submitter to project {project.name} by {request.user.get_full_name()}")

            msg = "Roles successfully assigned!"
    else:
        form = PMProjectManagmentForm(user=request.user)
    
    return render(request, template, {"form":form, "msg":msg, "users": User.objects.all()})