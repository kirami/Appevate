from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Payout
from .serializers import PayoutSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class PayoutViewSet(viewsets.ModelViewSet):
    model = Payout
    serializer_class = PayoutSerializer
    queryset = Payout.objects.all()
    



class PayoutList(generics.ListCreateAPIView):


    """
    get:
    Return a list of existing Payment, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspaccount-  Id of the Account you'd like to search for Payment<br>
    &nbsp &nbspplatform - Name of the Payment to search for.<br>
    

    post:
    Create a new Payment instance.
    """
    #permission_classes = (IsAuthenticated,) 
    serializer_class = PayoutSerializer
    
    def get_queryset(self):
        queryset = Payout.objects.all()
        app = self.request.query_params.get('app', None)
        #platform = self.request.query_params.get('app', None)
        

        if account is not None:
            queryset = queryset.filter(app=app)
        


        return queryset


class PayoutDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Payment

    put:
    Replacing entire Payment instance.

    patch:
    Update an Payment instance

    delete:
    Delete an Payment instance
    """
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = (IsAuthenticated,) 
