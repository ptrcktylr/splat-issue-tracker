from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.contrib.auth.models import User
from projects.models import Project
from simple_history.models import HistoricalRecords

PRIORITY_CHOICES = (('critical', 'Critical'),
                    ('major', 'Major'),
                    ('medium', 'Medium'),
                    ('minor', 'Minor'),
                    ('trivial', 'Trivial'))

TYPE_CHOICES = (('bug', 'Bug'),
                ('feature request', 'Feature Request'),
                ('customer issue', 'Customer Issue'),
                ('internal cleanup', 'Internal Cleanup'),
                ('process', 'Process'),
                ('vulnerability', 'Vulnerability'),)

STATUS_CHOICES = (('new', 'New'), # open
                  ('assigned', 'Assigned'), # open
                  ('accepted', 'Accepted'), # open
                  ('fixed', 'Fixed'), # closed
                  ('fixed (verified)', 'Fixed (Verified)'), # closed
                  ("won't fix (not reproducible)", "Won't Fix (Not reproducible)"), # closed
                  ("won't fix (intended behavior)", "Won't Fix (Intended behavior)"), # closed
                  ("won't fix (obsolete)", "Won't Fix (Obsolete)"), # closed
                  ("won't Fix (infeasible)", "Won't Fix (Infeasible)"), # closed
                  ('duplicate', 'Duplicate'),) # closed

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='bug')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='trivial')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')

    assigned_to = models.ForeignKey(User, on_delete=PROTECT, related_name='assigned_tickets', blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=PROTECT, related_name='submitted_tickets')

    project = models.ForeignKey(Project, on_delete=CASCADE, related_name='tickets')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content