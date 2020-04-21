

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Owner
from .serializers import OwnerSerializer

import logging

logger = logging.getLogger(__name__)


class OwnerViewSet(viewsets.ModelViewSet):
    model = Owner
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()


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
    



class OwnerList(generics.ListCreateAPIView):

    """
    get:
    Return a list of existing Owners, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the Owner you'd like to view<br>
    &nbsp &nbspuser - Id of the User who is associated as this Owner<br>
    &nbsp &nbspemail - Email of the Ownr which you'd like to search for.<br>

    

    post:
    Create a new Owner instance.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = OwnerSerializer
    
    def get_queryset(self):
        queryset = Owner.objects.all()
        user = self.request.query_params.get('user', None)
        email = self.request.query_params.get('email', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if user is not None:
            queryset = queryset.filter(user=user)
        if email is not None:
            queryset = queryset.filter(email=email)


        return queryset




class OwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Owner

    put:
    Replacing entire Owner instance.

    patch:
    Update an Owner instance

    delete:
    Delete an Owner instance
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = (IsAuthenticated,) 

