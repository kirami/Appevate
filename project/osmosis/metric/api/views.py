
from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Metric
from .serializers import MetricSerializer
from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger(__name__)


class MetricViewSet(viewsets.ModelViewSet):
    model = Metric
    serializer_class = MetricSerializer
    queryset = Metric.objects.all()


    '''
    def get_permissions(self):
        """
        Permissions for the ``User`` endpoints.

        - Allow create if the user is not authenticated.
        - Allow all if the user is staff.
        - Allow all if the user who is making the request is the same
            as the object in question.
        """

        return (permissions.AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),
    '''
    



class MetricList(generics.ListCreateAPIView):
    """
    get:
    Return a list of existing custom Metrics, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the custom Metric you'd like to view<br>
    &nbsp &nbspprogram - Id of the Program you'd like to search for custom Metrics defined<br>
    &nbsp &nbspname - Name of the custom Metric you'd like to search for<br>
    

    post:
    Create a new custom Metric instance.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = MetricSerializer
    
    def get_queryset(self):
        queryset = Metric.objects.all()
        first = self.request.query_params.get('host', None)
        second = self.request.query_params.get('second', None)
        name = self.request.query_params.get('name', None)
        program = self.request.query_params.get('program', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if name is not None:
            queryset = queryset.filter(name=name)
        if first is not None:
            queryset = queryset.filter(first=first)
        if second is not None:
            queryset = queryset.filter(second=second)
        if program is not None:
            queryset = queryset.filter(program=program)

        return queryset


class MetricDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Metric

    put:
    Replacing entire Metric instance.

    patch:
    Update an Metric instance

    delete:
    Delete an Metric instance
    """
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = (IsAuthenticated,) 
