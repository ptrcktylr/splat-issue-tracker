from django.shortcuts import render

def ticket(request):
    return render(request, 'tickets/ticket.html')

def tickets(request):
    return render(request, 'tickets/tickets.html')