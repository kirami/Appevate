from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
    model = Payment
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    



class PaymentList(generics.ListCreateAPIView):


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
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        queryset = Payment.objects.all()
        account = self.request.query_params.get('name', None)
        platform = self.request.query_params.get('platform', None)
        

        if account is not None:
            queryset = queryset.filter(account=account)
        if platform is not None:
            queryset = queryset.filter(platform=platform)
       


        return queryset


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Payment

    put:
    Replacing entire Payment instance.

    patch:
    Update an Payment instance

    delete:
    Delete an Payment instance
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,) 
