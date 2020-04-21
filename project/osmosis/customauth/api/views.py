
from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .permissions import AuthenticateKeys
from osmosis.app.api.serializers import TokenSerializer, VerificationSerializer
from ..models import User
from osmosis.utils import encrypt_val, decrypt_val
from django.db import IntegrityError
from django.db.models import Q

#from django.contrib.auth import get_user_model

import logging
logger = logging.getLogger('django')


#User = get_user_model


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpResponse
from osmosis.app.models import App


class VerifyIntegration(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = VerificationSerializer
     

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
       
        try:
            logger.info("VerifyIntegration")
            serializer.is_valid(raise_exception=True)
            logger.info(serializer)
            api_key = serializer.validated_data["api_key"]
           
            app = App.objects.get(api_key=api_key)
            app.integration_verified = True
            app.save()
            

        except Exception as e:
            logger.info(e)
            return HttpResponse(status=403)

        
        return HttpResponse(status=200)


    def get_queryset(self):
        
        

        return None

class CustomAuthToken(generics.ListCreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        #serializer.is_valid(raise_exception=True)
        #user = serializer.validated_data['user']
        user = None
        try:
            
            serializer.is_valid(raise_exception=True)
            key = serializer.validated_data['api_key']
            secret = serializer.validated_data['api_secret']
            app = App.objects.get(api_key = key)

            #logger.info("secret given: %s" % secret)
            #logger.info("secret in db: %s" % app.api_secret)
            #logger.info("given secret encrypted: %s" % encrypt_val(secret))
            if app.api_secret == encrypt_val(secret):
                #logger.info("matches")
                user = app.owner.user
            else:
                #logger.info("doesn't match")
                return HttpResponse(status=402)

        except Exception as e:
            logger.info(e)
            return HttpResponse(status=401)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })


    def get_queryset(self):
        
        

        return None

"""
class CustomAuthToken2(ObtainAuthToken):

    serializer_class = TokenSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        #serializer.is_valid(raise_exception=True)
        #user = serializer.validated_data['user']
        user = None
        try:
            key = request.GET.get("api_key")
            secret = request.GET.get("api_secret")
            app = App.objects.get(api_key = key)
            logger.info(app.api_secret)
            logger.info(encrypt_val(secret))
            if app.api_secret == encrypt_val(secret):
                user = app.owner.user
            else:
                return HttpResponse(status=400)
        except Exception as e:
            logger.info(e)
            return HttpResponse(status=401)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
"""

class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    
    

class UserList(generics.ListCreateAPIView):
    """
    get:
    Return a list of existing User, filtered by any parameter sent.<br>

    Possible Parameters - <br>
    &nbsp &nbspid -  Id of the User you'd like to view<br>
    &nbsp &nbspemail - Email of the User to search for.<br>
   

    post:
    Create a new User instance.
    """
    #permission_classes = (IsAuthenticated,) 
    serializer_class = UserSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        
        email = self.request.query_params.get('email', None)
        phone = self.request.query_params.get('phone_number', None)
        item_id = self.request.query_params.get('id', None)
        verified = self.request.query_params.get('verified', None)
        opted_in = self.request.query_params.get('opted_in', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        
        if verified is not None:
            queryset = queryset.filter(verified=verified)
        if opted_in is not None:
            queryset = queryset.filter(opted_in=opted_in)

        if phone is not None and email is not None:
            queryset = queryset.filter(Q(phone_number=phone) | Q(email=email))
        
        elif phone is not None:
            queryset = queryset.filter(phone_number=phone)
        elif email is not None:
            queryset = queryset.filter(email=email)

        return queryset

    def create(self, request, *args, **kwargs):
        try:
            
            email = self.request.data.get('email', None)
            phone = self.request.data.get('phone_number', None)
            logger.info(email)

            if not email and not phone:
                content = {'errorCode': 410, 'errorMessage': "A user must have an email address or phone number"}
                return Response(content, 410)

            if email and len(User.objects.filter(email=email)) > 0:
                content = {'errorCode': 411, 'errorMessage': "A user with this email already exists"}
                return Response(content, 411) 
            
            if phone and len(User.objects.filter(phone_number = phone)) > 0:
                content = {'errorCode': 412, 'errorMessage': "A user with the phone number already exists"}
                return Response(content, status=412) 

            return super(generics.ListCreateAPIView,self).create(request, *args, **kwargs)
        except IntegrityError as e:
            content = {'errorCode': errorCode, 'errorMessage': e}
            return Response(content, status=400) 

    def perform_create(self, serializer):
        serializer.save()



class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single User

    put:
    Replacing entire User instance.

    patch:
    Update an User instance

    delete:
    Delete an User instance
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,) 
