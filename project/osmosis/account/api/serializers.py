from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Account

import logging
logger = logging.getLogger(__name__)




class AccountSerializer(serializers.ModelSerializer):
    #user = serializers.CharField(default='')
    #contact_name = serializers.CharField(default='')

    class Meta:
        model = Account
        fields = ('id','user', 'balance', 'program')
        write_only_fields = ()
        read_only_fields = (
            
        )



