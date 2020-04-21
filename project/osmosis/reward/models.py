from django.db import models

# Create your models here.
class Reward(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
    