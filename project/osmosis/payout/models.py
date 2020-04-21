from django.db import models
from django.conf import settings
from osmosis.app.models import App


class Payout(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App, related_name='payout_app', on_delete=models.PROTECT)
    
    amount = models.DecimalField(
        max_digits=9, decimal_places=2
    ) 

    def __unicode__(self):
        return  str(self.id)