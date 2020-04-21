from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Payout

import logging
logger = logging.getLogger(__name__)


class PayoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payout
        fields = ('id','created', 'app', 'amount')
        write_only_fields = ()
        read_only_fields = (     
        )

