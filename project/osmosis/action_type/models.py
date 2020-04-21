from django.db import models
from django.conf import settings
from osmosis.app.models import App
from osmosis.program.models import Program
class ActionType(models.Model):
	created = models.DateTimeField(auto_now_add=True, help_text=("Date and Time Creatd"))
	name = models.CharField(max_length=64, db_index=True, help_text=("Descriptive name of this ActionType"))
	app = models.ForeignKey(App, related_name='actionType_app', on_delete=models.PROTECT, help_text=("*Ignore*"))
	program = models.ForeignKey(Program, related_name='actionType_program', on_delete=models.PROTECT, help_text=("Program this ActionType was defined for"))
	value = models.DecimalField(
		max_digits=9, decimal_places=2, help_text=("How much this ActionType is worth in decimal format"))
	description =  models.CharField(max_length=64, db_index=True, help_text=("Explanation of the ActionType"))
	def __unicode__(self):
		return self.name
	
