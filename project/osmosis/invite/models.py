from django.db import models
from django.conf import settings

class Invite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey('event.Event', on_delete=models.PROTECT, related_name='invite_event')
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='invite_user')

    def __unicode__(self):
        return str(self.id)