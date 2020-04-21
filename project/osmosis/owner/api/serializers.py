from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Owner

import logging
logger = logging.getLogger(__name__)




class OwnerSerializer(serializers.ModelSerializer):
    #user = serializers.CharField(default='')
    #contact_name = serializers.CharField(default='')

    class Meta:
        model = Owner
        fields = ('id','created', 'email', 'phone', 'user')
        write_only_fields = ()
        read_only_fields = (
            
        )



