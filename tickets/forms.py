from django import forms
from django.forms import fields, widgets
from .models import Comment, Ticket, Attachment

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

class AdminTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('project', 'title', 'description', 'assigned_to', 'type', 'priority',)

        widget = {
            'project': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'assigned_to': forms.Select(attrs={'class':'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
            'priority': forms.Select(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('ticket', 'content',)

        widget = {
            'ticket': forms.Select(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('ticket', 'image', 'note',)

        widget = {
            'ticket': forms.Select(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'note':forms.Textarea(attrs={'class':'form-control'}),
        }