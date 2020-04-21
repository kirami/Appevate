from django.contrib import admin
from .models import Payment
from osmosis.account.ledger.models import Ledger



from osmosis.app.models import App
from osmosis.program.models import Program

import logging
logger = logging.getLogger("django")

class PaymentAppFilter(admin.SimpleListFilter):
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
			a = Ledger.objects.filter(action__action_type__app=self.value()).values_list("payment")
			return Payment.objects.filter(pk__in=a)

class PaymentProgramFilter(admin.SimpleListFilter):
	title = 'Program'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'program'

	def lookups(self, request, model_admin):
		if "app" in request.GET: 
			apps = set([c for c in Program.objects.filter(app=request.GET["app"])])
		else:
			apps = set([c for c in Program.objects.all()])
		return [(b.id, b.name) for b in apps]

	def queryset(self, request, queryset):
		if not self.value():
			return queryset
		else:
			a = Ledger.objects.filter(action__action_type__program=self.value()).values_list("payment")
			return Payment.objects.filter(pk__in=a)



class PaymentAdmin(admin.ModelAdmin):

  list_display = ['id','created', 'platform', 'amount']
  list_filter =  (PaymentAppFilter, PaymentProgramFilter)

admin.site.register(Payment, PaymentAdmin)