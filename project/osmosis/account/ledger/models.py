from django.db import models
from django.conf import settings

from osmosis.action.models import Action
from osmosis.payout.models import Payout
from osmosis.payment.models import Payment

# Create your models here.
class Ledger(models.Model):
	created = models.DateTimeField(auto_now_add=True, help_text=("Date and Time Created"))
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ledger_user', help_text=("User object associated to this Ledger")) 
	amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text=("The amount given for performing the Action, in decimal format")
    )
	action = models.ForeignKey(Action, related_name='ledger_user', on_delete=models.PROTECT, help_text=("Action under which this Ledger item was made")) 
	payment = models.ForeignKey(Payment, blank=True, null = True, on_delete=models.PROTECT, related_name='ledger_payment', help_text=("Which payment paid this ledger item")) 
	payout = models.ForeignKey(Payout, blank=True, null = True, on_delete=models.PROTECT, related_name='ledger_payout', help_text=("Which payout paid for this ledger item")) 
	def __unicode__(self):
		return str(self.id)