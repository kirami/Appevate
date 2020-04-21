from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Payment

import logging
logger = logging.getLogger(__name__)


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ('id','created', 'platform', 'amount')
        write_only_fields = ()
        read_only_fields = (     
        )

