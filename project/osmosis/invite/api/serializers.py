from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Invite

import logging
logger = logging.getLogger(__name__)




class InviteSerializer(serializers.ModelSerializer):
    #user = serializers.CharField(default='')
    #contact_name = serializers.CharField(default='')

    class Meta:
        model = Invite
        fields = ('id','created', 'user')
        write_only_fields = ()
        read_only_fields = (
            
        )



