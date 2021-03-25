from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Notification(models.Model):
    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
