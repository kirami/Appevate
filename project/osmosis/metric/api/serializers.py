from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Metric

import logging
logger = logging.getLogger(__name__)




class MetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metric
        fields = ('id','created', 'name', 'program', 'first', 'second')
        write_only_fields = ()
        read_only_fields = (
            
        )



