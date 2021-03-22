from django import forms
from django.forms import fields, widgets
from .models import Project
from django.contrib.auth.models import User, Group

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')

        widget = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }

class AdminProjectManagmentForm(forms.Form):
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
    )

    admins = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='admin').all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
        required = False,
        
    )

    project_managers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='project manager').all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
        required = False,
    )

    developers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='developer').all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
        required = False,
    )

    submitters = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='submitter').all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
        required = False,
    )

class PMProjectManagmentForm(forms.Form):

    # this init limits projects to the project managers assigned projects only
    def __init__(self, user=None, *args, **kwargs):
        super(PMProjectManagmentForm, self).__init__(**kwargs)
        self.fields['projects'].queryset = user.assigned_projects.all()

    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
    )

    developers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='developer').all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
        required = False,
    )

    submitters = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='submitter').all(),
        widget=forms.SelectMultiple(attrs={'class':'form-control select-multiple'}),
        required = False,
    )