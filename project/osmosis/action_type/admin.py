from django.contrib import admin
from .models import ActionType
from osmosis.app.models import App
from osmosis.program.models import Program

import logging
logger = logging.getLogger("django")

class ATFilter(admin.SimpleListFilter):
	title = 'App'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'app'

	def lookups(self, request, model_admin):
		apps = set([c for c in App.objects.all()])
		return [(b.id, b.name) for b in apps]

	def queryset(self, request, queryset):
		
		if not self.value():
			return queryset
		else:
			return queryset.filter(program__app=self.value())

class ATProgramFilter(admin.SimpleListFilter):
	title = 'Program'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'program'

	def lookups(self, request, model_admin):
		logger.info( request.GET)
		if "app" in request.GET: 
			apps = set([c for c in Program.objects.filter(app=request.GET["app"])])
		else:
			apps = set([c for c in Program.objects.all()])
		return [(b.id, b.name) for b in apps]

	def queryset(self, request, queryset):
		logger.info(self.value())
		if not self.value():
			return queryset
		else:
			return queryset.filter(program=self.value())
	    

class ActionTypeAdmin(admin.ModelAdmin):

  list_display = ['id','app', 'name']
  search_fields = ['app__name', 'name']
  list_filter =  (ATFilter, ATProgramFilter) 


admin.site.register(ActionType, ActionTypeAdmin)