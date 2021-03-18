from django import forms
from django.forms import fields, widgets
from .models import Ticket

class TicketFormWithProject(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'type', 'priority')

        widget = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
            'priority': forms.Select(attrs={'class':'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('project', 'title', 'description', 'type', 'priority')

        widget = {
            'project': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
            'priority': forms.Select(attrs={'class':'form-control'}),
        }