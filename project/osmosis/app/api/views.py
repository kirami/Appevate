from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import App
from .serializers import AppSerializer
from django.shortcuts import get_object_or_404
from osmosis.utils import encrypt_val, decrypt_val

import logging

logger = logging.getLogger(__name__)


class AppViewSet(viewsets.ModelViewSet):
    model = App
    serializer_class = AppSerializer
    queryset = App.objects.all()


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
    
class RetrieveModelMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
       
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        obj = get_object_or_404(queryset)  # Lookup the object
        obj.api_secret = encrypt_val(obj.api_secret)
        self.check_object_permissions(self.request, obj)
        return obj


class AppList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,) 

    """
    get:
    Return a list of existing Apps, filtered by any paramater sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the App you'd like to view<br>
    &nbsp &nbspOwner - Id of the Owner you'd like to search for Apps<br>
    &nbsp &nbspName - Name of the App you'd like to search for<br>
    

    post:
    Create a new App instance.
    """

    serializer_class = AppSerializer
    
    def get_queryset(self):
        api_key = self.request.query_params.get('api_key', None)
        queryset = App.objects.filter(api_key=api_key)
        owner = self.request.query_params.get('owner', None)
        name = self.request.query_params.get('name', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if name is not None:
            queryset = queryset.filter(name=name)
        if owner is not None:
            queryset = queryset.filter(owner=owner)

        return queryset

    def get_object(self):
        logger.info("get object")
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            logger.info(field)

        obj = get_object_or_404(queryset, **filter)
        logger.info("secret %s" % obj["api_secret"])
        self.check_object_permissions(self.request, obj)
        return obj




class AppDetail(RetrieveModelMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single App

    put:
    Replacing entire App instance.

    patch:
    Update an App instance

    delete:
    Delete an App instance
    """
    serializer_class = AppSerializer
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        queryset = App.objects.filter(pk=self.kwargs["pk"])
        return queryset

    """
    def get(self, request, *args, **kwargs):
        logger.info("detail get")
        context = {}
        serializer = AppSerializer(
                data=request.data,
                context=context
            )
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response("bad", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    """


    