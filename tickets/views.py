from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

@login_required(login_url='/login/')
def ticket(request):
    return render(request, 'tickets/ticket.html')

@login_required(login_url='/login/')
def tickets(request):
    return render(request, 'tickets/tickets.html')