from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Program
from .serializers import ProgramSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class ProgramViewSet(viewsets.ModelViewSet):
    model = Program
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()


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
    



class ProgramList(generics.ListCreateAPIView):


    """
    get:
    Return a list of existing Programs, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the Program you'd like to view<br>
    &nbsp &nbspname - Name of the Program to search for.<br>
    &nbsp &nbspapp - Id of the App you'd like to search for Programs<br>
    &nbsp &nbspis_active - Boolean, search for only active programs or not.<br>
    

    post:
    Create a new Program instance.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = ProgramSerializer
    
    def get_queryset(self):
        queryset = Program.objects.all()
        name = self.request.query_params.get('name', None)
        app = self.request.query_params.get('app', None)
        item_id = self.request.query_params.get('id', None)
        is_active = self.request.query_params.get('is_active', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if name is not None:
            queryset = queryset.filter(name=name)
        if app is not None:
            queryset = queryset.filter(app=app)
        if is_active is not None:
            queryset = queryset.filter(isActive=is_active)


        return queryset


class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Program

    put:
    Replacing entire Program instance.

    patch:
    Update an Program instance

    delete:
    Delete an Program instance
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = (IsAuthenticated,) 
