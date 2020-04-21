from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Ledger
from .serializers import LedgerSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class LedgerViewSet(viewsets.ModelViewSet):
    model = Ledger
    serializer_class = LedgerSerializer
    queryset = Ledger.objects.all()


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
    



class LedgerList(generics.ListCreateAPIView):

    """
    get:
    Return a list of existing Ledgers, filtered by any paramater sent<br>
    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the Account you'd like to view<br>
    &nbsp &nbspuser - Id of the User you'd like to search for Accounts<br>

    post:
    Create a new Ledger instance.
    """

    serializer_class = LedgerSerializer
    permission_classes = (IsAuthenticated,) 
    
    def get_queryset(self):
        queryset = Ledger.objects.all()
        user = self.request.query_params.get('user', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if user is not None:
            queryset = queryset.filter(user=user)


        return queryset


class LedgerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Ledger object

    put:
    Replacing entire Ledger instance.

    patch:
    Update an existing Ledger instance

    delete:
    Delete a Ledger instance
    """
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    permission_classes = (IsAuthenticated,) 

