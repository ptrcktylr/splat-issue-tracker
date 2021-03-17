from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    assigned_users = models.ManyToManyField(User, related_name='assigned_projects', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk':self.pk})
    
    def num_open_tickets(self):
        return self.tickets.filter(Q(status='new') | Q(status='assigned') | Q(status='accepted') ).count()
    
   