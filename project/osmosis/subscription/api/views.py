from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class SubscriptionViewSet(viewsets.ModelViewSet):

    """
    Get Detail of single advertiser
    """
    
    model = Subscription
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


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
    



class SubscriptionList(generics.ListCreateAPIView):

    """
    get:
    Return a list of existing accounts, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the Subscription you'd like to view<br>
    &nbsp &nbspuser - Id of the User you'd like to search for Subscriptions<br>
    

    post:
    Create a new Subscription instance.
    """

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,) 
    
    
    
    def get_queryset(self):
        """
        Optionally restricts the returned Subscription to a given set of paramaters,
        by filtering against a `user` query parameter in the URL.
        """
        queryset = Subscription.objects.all()
        """
        user = self.request.query_params.get('user', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if user is not None:
            queryset = queryset.filter(user=user)
        """

        return queryset


class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Subscription

    put:
    Replacing entire Subscription instance.

    patch:
    Update an Subscription instance

    delete:
    Delete an Subscription instance
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,) 


