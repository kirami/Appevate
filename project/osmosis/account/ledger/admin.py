from django.contrib import admin

from .models import Ledger


class PaymentFilter(admin.SimpleListFilter):
	title = 'has payment'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'payment__isnull'

	def lookups(self, request, model_admin):
	    return (
	        ('False', 'has payment'),
	        ('True', 'has no payment'),
	    )

	def queryset(self, request, queryset):
	    if self.value() == 'False':
	        return queryset.filter(payment__isnull=False)
	    if self.value() == 'True':
	        return queryset.filter(payment__isnull=True)

class PayoutFilter(admin.SimpleListFilter):
	title = 'has payout'
	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'payout__isnull'

	def lookups(self, request, model_admin):
	    return (
	        ('False', 'has payout'),
	        ('True', 'has no payout'),
	    )

	def queryset(self, request, queryset):
	    if self.value() == 'False':
	        return queryset.filter(payout__isnull=False)
	    if self.value() == 'True':
	        return queryset.filter(payout__isnull=True)

class LedgerAdmin(admin.ModelAdmin):

  list_display = ['id','created', 'user', 'payout', 'payment']
  search_fields = ['user__email']
  list_filter =  (PaymentFilter, PayoutFilter) 





admin.site.register(Ledger, LedgerAdmin)