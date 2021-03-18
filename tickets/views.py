from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView
from .models import Ticket, Project
from .forms import TicketForm, TicketFormWithProject

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

class TicketCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.status = 'new'
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Ticket
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.status = 'new'
        form.instance.submitted_by = self.request.user
        return super().form_valid(form)

class TicketWithProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Ticket
    form_class = TicketFormWithProject

    def form_valid(self, form, *args, **kwargs):
        form.instance.status = 'new'
        form.instance.submitted_by = self.request.user
        form.instance.project = Project.objects.filter(id = self.kwargs['pk']).first() # gets project id as pk from project.urls
        return super().form_valid(form)