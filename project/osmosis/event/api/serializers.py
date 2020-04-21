from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Event

import logging
logger = logging.getLogger(__name__)


class EventSerializer(serializers.ModelSerializer):


    class Meta:
        model = Event
        fields = ('id','created', 'start_time', 'end_time', 'host')
        write_only_fields = ()
        read_only_fields = (
            
        )



