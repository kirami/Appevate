from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Program

import logging
logger = logging.getLogger(__name__)


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ('id','created', 'name', 'budget', 'app', 'CPA', 'CPC', 'CPM', 'isActive', 'css_url', 'CPC_max', 'CPM_max', 'CPA_max')
        write_only_fields = ()
        read_only_fields = (
            
        )

