from django.db import models
from django.conf import settings
from osmosis.app.models import App


class Payment(models.Model):
    PLATFORM_CHOICES = (
        ('PayPal', 'PayPal'),
    )


    created = models.DateTimeField(auto_now_add=True)
    #account = models.ForeignKey(Account, related_name='payment_account')
    #app = models.ForeignKey(App, related_name='payment_app')
    batch_id = models.CharField(max_length=26, blank=True)
    platform = models.CharField(
        max_length=12,
        choices=PLATFORM_CHOICES,
        default='',
        blank=False
    )
    amount = models.DecimalField(
        max_digits=9, decimal_places=2
    ) 

    def __unicode__(self):
        return  str(self.id)