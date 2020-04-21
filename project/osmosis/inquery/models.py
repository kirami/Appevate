from django.db import models

# Create your models here.
class Inquery(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(
        verbose_name='email address',
        unique=False,
        max_length=255,
        blank=True,
        null=True,
        help_text=("Email address for this User"))
    name = models.CharField(max_length=75, null=True, blank=True, help_text=("Contact name"))
    
    subject = models.CharField(max_length=75, null=True, blank=True, help_text=("Inquery subject"))
    
    message  = models.TextField(max_length=200, null=True, blank=True, help_text=("Inquery message"))
    

    def __unicode__(self):
        return self.subject
    
    class Meta:
        verbose_name_plural = "Inqueries"