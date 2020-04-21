from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Action

import logging
logger = logging.getLogger(__name__)




class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ('id','created', 'action_type', 'fromUser', 'toUser', 'name', 'event')
        write_only_fields = ()
        read_only_fields = (
            
        )



