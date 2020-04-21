from django.contrib import admin
from .models import Action

from osmosis.app.models import App
from osmosis.program.models import Program

import logging
logger = logging.getLogger("django")

class ActionFilter(admin.SimpleListFilter):
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
			return queryset.filter(action_type__program__app=self.value())

class ActionProgramFilter(admin.SimpleListFilter):
	title = 'Program'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'program'

	def lookups(self, request, model_admin):
		#logger.info( request.GET)
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
			return queryset.filter(action_type__program=self.value())

class UserFilter(admin.SimpleListFilter):
	title = 'User'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'userOnly'

	def lookups(self, request, model_admin):
		return (
	        ('1', 'from only'),
	        ('2', 'to and from'),
	    )

	def queryset(self, request, queryset):
		val = request.GET.get("userOnly",None)
		logger.info("val: %s" % val)
		if val:
			if val == "1":
				return queryset.filter(toUser__isnull=True)
			else:
				return queryset.filter(toUser__isnull=False)
		return queryset
	    


class ActionAdmin(admin.ModelAdmin):

  list_display = ['id','created', 'fromUser', 'toUser']
  search_fields = ['fromUser__email', 'toUser__email']
  list_filter =  (ActionFilter, ActionProgramFilter, UserFilter)


admin.site.register(Action, ActionAdmin)