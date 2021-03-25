from .models import Notification

def create_notification(request, to_user, message):
    notification = Notification.objects.create(to_user=to_user, message=message, created_by=request.user)