from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Ledger

import logging
logger = logging.getLogger(__name__)




class LedgerSerializer(serializers.ModelSerializer):
    #user = serializers.CharField(default='')
    #contact_name = serializers.CharField(default='')

    class Meta:
        model = Ledger
        fields = ('id','user', 'amount', 'action')
        write_only_fields = ()
        read_only_fields = (
            
        )



