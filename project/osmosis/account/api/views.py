from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class AccountViewSet(viewsets.ModelViewSet):

    """
    Get Detail of single advertiser
    """
    
    model = Account
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


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
    



class AccountList(generics.ListCreateAPIView):

    """
    get:
    Return a list of existing accounts, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the Account you'd like to view<br>
    &nbsp &nbspuser - Id of the User you'd like to search for Accounts<br>
    

    post:
    Create a new Account instance.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = AccountSerializer

    def list(self):
        """
        user -- A first parameter
        param2 -- A second parameter
        """ 
    
    
    def get_queryset(self):
        """
        Optionally restricts the returned Account to a given set of paramaters,
        by filtering against a `user` query parameter in the URL.
        """
        queryset = Account.objects.all()
        user = self.request.query_params.get('user', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if user is not None:
            queryset = queryset.filter(user=user)


        return queryset


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Account

    put:
    Replacing entire Account instance.

    patch:
    Update an Account instance

    delete:
    Delete an Account instance
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,) 

