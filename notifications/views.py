from django.http import request
from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != "":
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

    return render(request, 'notifications/notification.html')

class NotificationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = '/login/'
    model = Notification
    template_name = "notifications/notification_detail.html"

    def read_message(self, request):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
    
    def test_func(self):
        notification = self.get_object()

        if self.request.user == notification.to_user:
            self.read_message(request)

        return (self.request.user == notification.to_user)