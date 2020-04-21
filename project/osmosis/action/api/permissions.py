from rest_framework import permissions
from osmosis.app.models import App


import logging
logger = logging.getLogger(__name__)

class AuthenticateKeys(permissions.BasePermission):
    def has_permission(self, request, view):
        
        key = request.GET.get("api_key")
        secret = request.GET.get("api_secret")

       	try:
        	app = App.objects.get(api_key = key)
        	return app.api_secret == secret
        except:
        	#logger.info("returning false")
        	return False


    