from django.db import models
from django.conf import settings
from osmosis.owner.models import Owner
from osmosis.utils import encrypt_val, decrypt_val
#from osmosis.program.models import Program

import logging
logger = logging.getLogger(__name__)

class App(models.Model):


    UI_CHOICES = (
        ("0","Default"),
        ("1", "Apple"),
        ("2", "Red"),
        ("3", "Custom"),
    )

    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=64, db_index=True, blank=True, null=True, help_text=("URL of this App"))
    name = models.CharField(max_length=64, db_index=True, help_text=("Name of this App"))
    css_url = models.CharField(max_length=64, db_index=True, blank=True, help_text=("A URL pointing to customized CSS that will overwrite the current styles"))
    owner = models.ForeignKey(Owner, related_name='app_owner', on_delete=models.PROTECT, help_text=("Owner of the App"))
    self_payout = models.BooleanField(default=False, help_text=(""))
    api_secret = models.CharField(max_length=64, db_index=True, blank=True, help_text=("API Key for this App"))
    api_key = models.CharField(max_length=64, db_index=True, blank=True, help_text=("API Secret for this App"))
    image = models.ImageField(upload_to='store_images',null=True, blank=True, help_text=("Image uploaded for this App"))
    stripe_id = models.CharField(max_length=64, db_index=True, blank=True, help_text=("Id for the Stripe Account associated with this App"))
    stripe_account = models.CharField(max_length=64, db_index=True, blank=True, help_text=("Identifier for the Stripe Account associated with this App"))
    ui_style  = models.CharField(
        max_length=12,
        choices=UI_CHOICES,
        default=0,
        blank=False
    )

    custom_color = models.CharField(max_length=10, db_index=True, blank=True, help_text=("Custom Theme Color"))
    integration_verified = models.BooleanField(default=False, help_text=("Has this app made a successful api call"))
    

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.api_secret = encrypt_val(self.api_secret)
        super(App, self).save(*args, **kwargs)
    """
    def get_active_program(self):
        return Program.obects.filter(app=self, is_active=True)[0]


    def get_all_programs(self):
        return Program.obects.filter(app=self)
    """
