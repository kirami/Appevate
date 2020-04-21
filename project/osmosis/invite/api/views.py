from rest_framework import viewsets, permissions



from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Invite
from .serializers import InviteSerializer

import logging

logger = logging.getLogger(__name__)

 

"""

class InviteList(generics.ListCreateAPIView):

    serializer_class = InviteSerializer
    
    def get_queryset(self):
        queryset = Invite.objects.all()
        event = self.request.query_params.get('event', None)
        user = self.request.query_params.get('user', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if event is not None:
            queryset = queryset.filter(event=event)
        if user is not None:
            queryset = queryset.filter(user=user)


        return queryset




class InviteDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer


"""