from django.db import models
from django.conf import settings
from osmosis.program.models import Program

# Create your models here.
class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(help_text=("Start time of Event"))
    end_time = models.DateTimeField(help_text=("End Time of Event"))
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='event_host', help_text=("The User who owns this Event"))
    program = models.ForeignKey(Program, related_name='event_program', on_delete=models.PROTECT,help_text=("The Program this Event is run under"))
    name = models.CharField(max_length=64, db_index=True, help_text=("Descriptive name of the Event"))
    
    def __unicode__(self):
        return self.name