#from django.contrib.auth import get_user_model
from ..models import User
from rest_framework import serializers


import logging
logger = logging.getLogger(__name__)




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','created', 'email', 'paypal_email', "venmo_email", 'phone_number', 'opted_in', 'accepted')
        write_only_fields = ()
        read_only_fields = ('verify_code',)



