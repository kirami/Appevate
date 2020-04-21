from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from model_utils.models import TimeStampedModel
from django.db.models import Sum

from osmosis.account.ledger.models import Ledger

import logging, uuid
logger = logging.getLogger('django')
# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, phone_number, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given phone_number, email and password.
        """
        #email = self.normalize_email(email) if email else ''
        #phone_number = username or ''
        user = self.model(phone_number=phone_number, email=email,
                          is_staff=is_staff, is_active=True,
                          is_admin=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None,
                    **extra_fields):
        """
        Creates and saves a User with the given email, and password.
        """
        logger.info("here1")
        if not email and not phone_number:
            logger.info("here")
            raise ValueError('Users must have an email address or phone_number')

        return self._create_user(phone_number, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username=None, email=None, password=None,
                         **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        if not email and not username:
            raise ValueError( 'must have an email address or username')

        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    #class Meta:
    #    unique_together = ('username', 'email')

    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=255,
        blank=True,
        null=True,
        help_text=("Email address for this User"))
    username = models.CharField(max_length=75, null=True, blank=True, help_text=("Username for this User"))
    phone_number = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text=("User's Phone Number"))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    verified = models.BooleanField(default=False, help_text=("Has this User's email been verified? "))
    verify_code = models.CharField(max_length=75, null=True, blank=True)
    opted_in = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    redeem_threshold = models.DecimalField(
        max_digits=9, decimal_places=2, help_text=("Threshold for auto redemption"), default=0
    )

    paypal_email = models.EmailField(
        verbose_name='Paypal email address',
        max_length=255,
        default='',
        blank=True,
        help_text=("Paypal Email for this User"))

    venmo_email = models.EmailField(
        verbose_name='Venmo email address',
        max_length=255,
        default='',
        blank=True,
        help_text=("Venmo Email address for this User"))

    objects = UserManager()

    USERNAME_FIELD = 'email'


    def save(self,  **kwargs):
        if not self.verify_code:
            self.verify_code = uuid.uuid4().hex
        super(User, self).save()


    def get_full_name(self):
        # The user is identified by their email address
        logger.info("full")
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        logger.info("short")
        return self.email

    def __unicode__(self):
        
        
        if self.email and self.email !="None":
            return self.email
        
        elif self.phone_number:
            return str(self.phone_number)

        else:
            return str(self.id)

    @property
    def get_redeemable(self):
        total = Ledger.objects.filter(user=self, payout__isnull=False, payment=None)
        if not total:
            return 0
        else:
            return total.aggregate(Sum('amount'))["amount__sum"]
    
    @property
    def get_total(self):
        total =  Ledger.objects.filter(user=self, payment=None)
        if not total:
            return 0
        else:
            return total.aggregate(Sum('amount'))["amount__sum"]
    
    @property
    def get_amount_paid(self):
        total =  Ledger.objects.filter(user=self, payment__isnull=False)
        if not total:
            return 0
        else:
            return total.aggregate(Sum('amount'))["amount__sum"]

    

    