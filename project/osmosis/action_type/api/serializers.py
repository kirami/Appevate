from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import ActionType

import logging
logger = logging.getLogger(__name__)


class ActionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionType
        fields = ('id','created', 'name', 'program', 'value', 'description')
        write_only_fields = ()
        read_only_fields = (
            
        )



