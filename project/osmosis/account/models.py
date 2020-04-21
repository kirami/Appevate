from django.db import models
from django.conf import settings
from osmosis.app.models import App
from osmosis.program.models import Program



class Account(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_user', on_delete=models.PROTECT, help_text=("User object associated to this account")) 
    program = models.ForeignKey(Program, related_name='account_program', on_delete=models.PROTECT, help_text=("The Program under which the User's Actions will be added to the Ledger."))
    balance = models.DecimalField(
        max_digits=9, decimal_places=2, help_text=("The amount owed, in decimal format")
    )

    def __unicode__(self):
        return str(self.id)