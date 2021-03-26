from django.contrib.auth import decorators
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from .models import Attachment, Comment, Ticket, Project
from django.contrib.auth.models import User
from .forms import AttachmentForm, CommentForm, TicketForm, TicketFormWithProject, AdminTicketForm
from authentication.decorators import admin_user, project_manager_user, developer_user, submitter_user
from notifications.utilities import create_notification

@login_required(login_url='/login/')
def ticket(request):
    return render(request, 'tickets/ticket.html')

@login_required(login_url='/login/')
def tickets(request):
    return render(request, 'tickets/tickets.html')

class TicketListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Ticket
    template_name = 'tickets/tickets.html'
    context_object_name = 'tickets'
    ordering = ['-created_at']

class TicketDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Ticket

decorators = [submitter_user]
@method_decorator(decorators, name='dispatch')
class TicketCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Ticket
    fields = ['project', 'title', 'description', 'type', 'priority']
    # form_class = TicketForm

    def get_form(self, *args, **kwargs):
        form = super(TicketCreateView, self).get_form(*args, **kwargs)

        # only let the submitters submit tickets for projects they're assigned to
        if self.request.user.groups.filter(name='admin').exists():
            form.fields['project'].queryset = Project.objects.all()
        else:
            form.fields['project'].queryset = self.request.user.assigned_projects.all()

        return form

    def form_valid(self, form):
        form.instance.status = 'new'
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = Ticket
    fields = ['project', 'title', 'description', 'type', 'priority']
    # form_class = TicketForm

    def get_form(self, *args, **kwargs):
        form = super(TicketUpdateView, self).get_form(*args, **kwargs)

        # only let the submitters submit tickets for projects they're assigned to
        if self.request.user.groups.filter(name='admin').exists():
            form.fields['project'].queryset = Project.objects.all()
        else:
            form.fields['project'].queryset = self.request.user.assigned_projects.all()

        return form

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        ticket = self.get_object()
        return (self.request.user == ticket.submitted_by) or (ticket.assigned_to == self.request.user)

class TicketAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = Ticket
    fields = ['project', 'title', 'description', 'assigned_to', 'type', 'priority', 'status']
    # form_class = AdminTicketForm

    def get_form(self, *args, **kwargs):
        form = super(TicketAdminUpdateView, self).get_form(*args, **kwargs)

        # project managers can only add ticket to projects they're assigned to 
        if self.request.user.groups.filter(name='admin').exists():
            form.fields['project'].queryset = Project.objects.all()
        else:
            form.fields['project'].queryset = self.request.user.assigned_projects.all()

        # only let developers be assigned to tickets
        form.fields['assigned_to'].queryset = User.objects.filter(groups__name='developer').all()
        return form

    def form_valid(self, form):
        user = form.cleaned_data['assigned_to']
        title = form.cleaned_data['title']

        try:
            create_notification(self.request, self.object.history.first().assigned_to, f"You have been unassigned from the ticket {title} by {self.request.user.get_full_name()}")
        except:
            pass
        create_notification(self.request, user, f"You have been assigned to the ticket {title} by {self.request.user.get_full_name()}")

        return super().form_valid(form)

    def test_func(self):
        ticket = self.get_object()
        return (self.request.user.groups.filter(name='admin').exists() or (self.request.user.groups.filter(name='project manager') and self.request.user in ticket.project.assigned_users.all()) )

@method_decorator(decorators, name='dispatch')
class TicketWithProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Ticket
    fields = ['project', 'title', 'description', 'type', 'priority']

    def get_form(self, *args, **kwargs):
        form = super(TicketWithProjectCreateView, self).get_form(*args, **kwargs)

        form.fields['project'].queryset = Project.objects.filter(id=self.kwargs['pk'])
        return form


    def form_valid(self, form, *args, **kwargs):
        form.instance.status = 'new'
        form.instance.submitted_by = self.request.user
        form.instance.project = Project.objects.filter(id = self.kwargs['pk']).first() # gets project id as pk from project.urls
        return super().form_valid(form)


class TicketDeveloperUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = Ticket
    fields = ['title', 'description', 'type', 'priority', 'status']

    def get_form(self, *args, **kwargs):
        form = super(TicketDeveloperUpdateView, self).get_form(*args, **kwargs)
        return form

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        ticket = self.get_object()
        return ( self.request.user.groups.filter(name='developer').exists() and ticket.assigned_to == self.request.user )

class CommentCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Comment
    form_class = CommentForm
    
    def get_form(self, *args, **kwargs):
        form = super(CommentCreateView, self).get_form(*args, **kwargs)

        form.fields['ticket'].queryset = Ticket.objects.filter(id=self.kwargs['pk'])
        return form
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class AttachmentCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Attachment
    form_class = AttachmentForm
    
    def get_form(self, *args, **kwargs):
        form = super(AttachmentCreateView, self).get_form(*args, **kwargs)
        form.fields['ticket'].queryset = Ticket.objects.filter(id=self.kwargs['pk'])
        return form
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)