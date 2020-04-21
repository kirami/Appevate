from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import ActionType
from .serializers import ActionTypeSerializer
from osmosis.program.models import Program


import logging
logger = logging.getLogger(__name__)


class OwnerViewSet(viewsets.ModelViewSet):
    model = ActionType
    serializer_class = ActionTypeSerializer
    queryset = ActionType.objects.all()


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
    



class ActionTypeList(generics.ListCreateAPIView):
    """
    get:
    Return a list of existing ActionTypes, filtered by any paramater sent<br>
    Possible Parameters - <br>
    &nbsp &nbspname-  Name of the ActionType you'd like to filter the list for.<br>

    &nbsp &nbspprogram - Id of the Program you'd like to search for ActionTypes<br>

    &nbsp &nbspid - Id of the ActionType you'd like to view<br>

    post:
    Create a new ActionType.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = ActionTypeSerializer

    def get_queryset(self):

        queryset = ActionType.objects.all()
        program = self.request.query_params.get('program', None)
        name = self.request.query_params.get('name', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if name is not None:
            queryset = queryset.filter(name=name)
        if program is not None:
            queryset = queryset.filter(app=program)

        return queryset


class ActionTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single ActionType object

    put:
    Replacing entire ActionType.

    patch:
    Update an existing ActionType

    delete:
    Delete a ActionType
    """
    queryset = ActionType.objects.all()
    serializer_class = ActionTypeSerializer
    permission_classes = (IsAuthenticated,) 



    