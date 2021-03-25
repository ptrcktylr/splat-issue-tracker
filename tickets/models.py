from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.contrib.auth.models import User
from projects.models import Project
from simple_history.models import HistoricalRecords
from django.urls import reverse

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
    
    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})
    
    # There's probably a better way to do this.. 
    # Priorities
    def num_critical(self):
        return self.__class__.objects.filter(priority='critical').count()
        
    def num_major(self):
        return self.__class__.objects.filter(priority='major').count()
    
    def num_medium(self):
        return self.__class__.objects.filter(priority='medium').count()
    
    def num_minor(self):
        return self.__class__.objects.filter(priority='minor').count()
    
    def num_trivial(self):
        return self.__class__.objects.filter(priority='trivial').count()
    
    # Statuses
    def num_new(self):
        return self.__class__.objects.filter(status='new').count()

    def num_assigned(self):
        return self.__class__.objects.filter(status='assigned').count()

    def num_accepted(self):
        return self.__class__.objects.filter(status='accepted').count()

    def num_fixed(self):
        return self.__class__.objects.filter(status='fixed').count()
    
    def num_fixed_v(self):
        return self.__class__.objects.filter(status='fixed (verified)').count()
    
    def num_wont_fix_nr(self):
        return self.__class__.objects.filter(status="won't fix (not reproducible)").count()
    
    def num_wont_fix_ib(self):
        return self.__class__.objects.filter(status="won't fix (intended behavior)").count()
    
    def num_wont_fix_o(self):
        return self.__class__.objects.filter(status="won't fix (obsolete)").count()

    def num_wont_fix_i(self):
        return self.__class__.objects.filter(status="won't fix (infeasible)").count()
    
    def num_duplicate(self):
        return self.__class__.objects.filter(status="duplicate").count()
    
    # Types
    def num_bugs(self):
        return self.__class__.objects.filter(type="bug").count()

    def num_feature_requests(self):
        return self.__class__.objects.filter(type="feature request").count()
    
    def num_customer_issues(self):
        return self.__class__.objects.filter(type="customer issue").count()

    def num_internal_cleanups(self):
        return self.__class__.objects.filter(type="internal cleanup").count()
    
    def num_processes(self):
        return self.__class__.objects.filter(type="process").count()
    
    def num_vulnerabilities(self):
        return self.__class__.objects.filter(type="vulnerability").count()
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('ticket-detail', args=[str(self.ticket.id)])

class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=CASCADE, related_name="attachments")
    image = models.ImageField(upload_to='attachment_pics')
    author = models.ForeignKey(User, on_delete=CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image.name[16:]

    def get_absolute_url(self):
        return reverse('ticket-detail', args=[str(self.ticket.id)])
