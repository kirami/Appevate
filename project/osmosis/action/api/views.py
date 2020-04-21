
from rest_framework import viewsets, permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from ..models import Action
from .serializers import ActionSerializer
from .permissions import AuthenticateKeys
from osmosis.action_type.models import ActionType
from osmosis.account.models import Account
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from osmosis.account.ledger.models import Ledger
from osmosis.customauth.models import User


import logging
#logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

class ActionViewSet(viewsets.ModelViewSet):
    model = Action
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    def create(self, request, *args, **kwargs):
        response = super(ModelViewSet, self).create(request, args, kwargs)
        logger.info("3 post saved: %s" % obj)
        return response

    def post_save(self, obj, created=False):
        logger.info("2 post saved: %s" % obj)
    '''
    def create(self, request):
        # do your thing here
        logger.info("create")
        return super().create(request)
    '''

    #def create(self, request, *args, **kwargs):

    
    
    

class ActionList(generics.ListCreateAPIView):
    """
    get:
    Return a list of existing Actions, filtered by any paramater sent<br>
    Possible Parameters - <br>
    &nbsp &nbspname-  Name of the Action you'd like to filter the list for.<br>
    &nbsp &nbspuser - Id of the User you'd like to search for Actions sent<br>
    &nbsp &nbsptoUser - Id of the User you'd like to search for Actions received<br>
    &nbsp &nbspprogram - Id of the Program you'd like to search for Actions<br>
    &nbsp &nbspevent - Id of the Event you'd like to search for Actions<br>
    &nbsp &nbspid - Id of the Action you'd like to view<br>

    post:
    Create a new Action instance.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = ActionSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Action.objects.all()
        user = self.request.query_params.get('fromUser', None)
        toUser = self.request.query_params.get('toUser', None)
        name = self.request.query_params.get('name', None)
        action = self.request.query_params.get('action', None)
        program = self.request.query_params.get('program', None)
        event = self.request.query_params.get('event', None)
        item_id = self.request.query_params.get('id', None)

        if item_id is not None:
            queryset = queryset.filter(id=item_id)
        if user is not None:
            queryset = queryset.filter(fromUser=user)
        if toUser is not None:
            queryset = queryset.filter(toUser=toUser)
        #name, action, program, event
        if name is not None:
            queryset = queryset.filter(name=name)
        if action is not None:
            queryset = queryset.filter(action=action)
        if program is not None:
            queryset = queryset.filter(program=program)
        if event is not None:
            queryset = queryset.filter(event=event)

        return queryset
    
    def perform_create(self, serializer):

        serializer.save()
        object_id = serializer.data["id"]
        at = ActionType.objects.get(pk=serializer.data["action_type"])
        #logger.info("s %s" % at.program)
        user_id = serializer.data["fromUser"]
        accounts = Account.objects.filter(user=user_id)

        user = User.objects.get(pk=user_id)
        if len(accounts) > 0:
            account = accounts[0]
        else:
            account = Account.objects.create(user = user, balance = 0, program = at.program)

        amount = Decimal(account.balance) + Decimal(at.value)
        account.balance = amount
        account.save()

        #add to ledger
        Ledger.objects.create(action=Action.objects.get(pk=object_id), amount = at.value, user = user)



   




class ActionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get Detail of single Action object

    put:
    Replacing entire Action instance.

    patch:
    Update an existing Action instance

    delete:
    Delete a Action instance
    """
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = (IsAuthenticated,) 
    
    def post_save(self, obj, created=False):
        logger.info("1 post saved: %s" % obj)
        


