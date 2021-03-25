from django.contrib import admin
from .models import Attachment, Ticket, Comment
from simple_history.admin import SimpleHistoryAdmin

class TicketHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["title", "description", "type", "priority", "status", "assigned_to", "project"]
    history_list_display = ["priority", "status", "assigned_to"]
    search_fields = ['title', 'assigned_to']

admin.site.register(Ticket, TicketHistoryAdmin)
admin.site.register(Comment)
admin.site.register(Attachment)