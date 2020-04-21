from django.db import models
from django.conf import settings
from osmosis.app.models import App



class Subscription(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App, related_name='subscription_app', on_delete=models.PROTECT, help_text=("The App this Subscription is under"))
	