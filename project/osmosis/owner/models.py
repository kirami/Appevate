from django.db import models
from django.conf import settings

# Create your models here.
class Owner(models.Model):
	created = models.DateTimeField(auto_now_add=True, help_text=(""))
	email = models.EmailField(
		verbose_name='email address',
		unique=True,
		max_length=255,
		default='',
		blank=True,
	 help_text=("Email address for this Owner"))
	phone =  models.CharField(max_length=20, blank=True, help_text=("Phone Number for this Owner"))
	first_name =  models.CharField(max_length=20, blank=True)
	last_name =  models.CharField(max_length=20, blank=True)

	CSS_URL  = models.CharField(max_length=200, blank=True)
	user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owner_user', help_text=("User associated with this Owner"))

	def __unicode__(self):
		return self.user.email