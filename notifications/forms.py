from django import forms
from .models import Notification
from django.contrib.auth.models import User

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('is_read')
        widgets = {'any_field': forms.HiddenInput()}