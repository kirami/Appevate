from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Subscription

import logging
logger = logging.getLogger(__name__)




class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id','created', 'app')
        write_only_fields = ()
        read_only_fields = (
            
        )



