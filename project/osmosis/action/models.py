from django.db import models
from django.conf import settings
from osmosis.program.models import Program
from osmosis.action_type.models import ActionType
from osmosis.event.models import Event

from datetime import datetime
import datetime as dt

class Action(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, db_index=True, blank=True, help_text=("Descriptive name of the Action taken"))
    action_type = models.ForeignKey(ActionType, related_name='actionType_action', on_delete=models.PROTECT, help_text=("The predefined type of Action taken"))
    #program = models.ForeignKey(Program, related_name='actionType_program', help_text=("The Program under which an Action was taken"))
    fromUser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='action_fromUser', on_delete=models.PROTECT, help_text=("The User who performed the defined Action"))
    toUser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='action_toUser',on_delete=models.PROTECT, null=True, help_text=("The User who received the defined Action"))
    event = models.ForeignKey(Event, related_name='actionType_event', on_delete=models.PROTECT, blank=True, null=True, help_text=("The Event associatd with this Action"))

    def __unicode__(self):
        return str(self.id)
    """
    def get_daily_data(self, program, action_type):
	        nums = [] 
	        series = []

	        today = dt.date.today()
	        weekday=today.weekday()

	        for i in reversed(range(7)):
	            day = today - dt.timedelta(days = i)
	            nums.append(day.weekday())

	        thisMonday=today - dt.timedelta(days=7)
	        for n in nums:
	            x = []
	            val = 0
	            x = self.objects.filter(**{"created__week_day": n, "program":program, "action_type":action_type })
	            val = len(x)
	            
	            series.append(val)

	        return series
	"""