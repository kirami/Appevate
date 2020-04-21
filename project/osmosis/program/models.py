from django.db import models
from django.conf import settings
from osmosis.app.models import App

class Program(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=64, db_index=True, help_text=("Descriptive Name of this Program"))
	app = models.ForeignKey(App, related_name='program_app', on_delete=models.PROTECT,help_text=("The App who runs this Program"))
	#budget = models.IntegerField(default=0, help_text=("The budget set for this program as an integer"))
	budget = models.DecimalField(
		max_digits=9, decimal_places=2, default=0, help_text=("The budget set for this program as an integer")
	) 
	CPA = models.BooleanField(default=False, help_text=("Are CPA's being tracked?"))
	CPC = models.BooleanField(default=False, help_text=("Are CPC's being tracked?"))
	CPM = models.BooleanField(default=False, help_text=("Are CPM's being tracked?"))
	isActive = models.BooleanField(default=False, help_text=("Is this Program active?"))
	CPA_max = models.IntegerField(default=0, help_text=("The max set for this program's CPA as an integer"))
	CPC_max = models.IntegerField(default=0, help_text=("The max set for this program's CPC as an integer"))
	CPM_max = models.IntegerField(default=0, help_text=("The max set for this program's CPM as an integer"))
	css_url = models.CharField(max_length=64, db_index=True, blank=True, help_text=("A URL pointing to customized CSS that will overwrite the current styles"))
	description = models.CharField(max_length=128, db_index=True, help_text=("Program Description"))
	

	def __unicode__(self):
		return self.name

	
