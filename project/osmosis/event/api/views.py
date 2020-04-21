from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class EventViewSet(viewsets.ModelViewSet):
    model = Event
    serializer_class = EventSerializer
    queryset = Event.objects.all()


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
    



class EventList(generics.ListCreateAPIView):

    """
    get:
    Return a list of existing Events, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the Event you'd like to view<br>
    &nbsp &nbsphost - Id of the User who is hosting an Event<br>
    &nbsp &nbspprogram - Program under which the Event is listed.<br>
    &nbsp &nbspname - Name of the Event you'd like to search for<br>
    

    post:
    Create a new Event instance.
    """

    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,) 
    
    def get_queryset(self):
        queryset = Event.objects.all()
        host = self.request.query_params.get('host', None)
        name = self.request.query_params.get('name', None)
        program = self.request.query_params.get('program', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if name is not None:
            queryset = queryset.filter(name=name)
        if host is not None:
            queryset = queryset.filter(host=host)
        if program is not None:
            queryset = queryset.filter(program=program)

        return queryset


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Event

    put:
    Replacing entire Event instance.

    patch:
    Update an Event instance

    delete:
    Delete an Event instance
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,) 

