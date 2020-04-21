from django.contrib import admin
from .models import Payout


from osmosis.app.models import App
from osmosis.program.models import Program

import logging
logger = logging.getLogger("django")

class PayoutAppFilter(admin.SimpleListFilter):
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
			return queryset.filter(app=self.value())


class PayoutAdmin(admin.ModelAdmin):

  list_display = ['id','created', 'app', 'amount']
  search_fields = ['app__name', 'app__id']
  list_filter =  (PayoutAppFilter,)

admin.site.register(Payout, PayoutAdmin)