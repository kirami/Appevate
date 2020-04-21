from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
import dwollav2


# Create your views here.
import logging, json, requests, md5, urllib2, urllib
logger = logging.getLogger(__name__)


def dwolla_get_account_href(app_token):
	links = app_token.get('/')
	href = links.body['_links']['account']['href']
	ind  = href.rfind("/")
	account = href[ind+1:]
	return href 

def dwolla_get_funding_sources(app_token, href):
	return app_token.get(href + '/funding-sources')

def dwolla_get_or_create_customer(app_token, form=None):
	request_body = {
	  'firstName': 'k',
	  'lastName': 'd',
	  'email': 'kira@sharemagnet.com',
	  'type': 'receive-only',
	}

	customer = app_token.post('customers', request_body)
	customer.headers['location']

#'https://api-sandbox.dwolla.com/customers/d71e5265-d0e8-413b-8025-761819ea17a3'
def dwolla_transfer():
	request_body = {
	  '_links': {
	    'source': {
	      'href': 'https://api-sandbox.dwolla.com/funding-sources/e3d4fafc-e246-48fd-b709-8f8392a54681'
	    },
	    'destination': {
	      'href': 'https://api-sandbox.dwolla.com/funding-sources/dea0b4c7-3183-4d47-bd43-03cb6f6f53a0'
	    }
	  },
	  'amount': {
	    'currency': 'USD',
	    'value': '1.00'
	  },
	  'metadata': {
	    'paymentId': '12345678',
	    'note': 'payment for completed work Dec. 1'
	  },
	  'clearing': {
	    'destination': 'next-available'
	  },
	 
	  'correlationId': '8a2cdc8d-629d-4a24-98ac-40b735229fe2'
	}

	transfer = app_token.post('transfers', request_body)


@login_required
def dwolla_payment(request):
	data = {}
	
	if request.method == "POST":
		client = dwollav2.Client(key = settings.DWOLLA_KEY,
                         secret = settings.DWOLLA_SECRET,
                         environment = settings.DWOLLA_ENV) # optional - defaults to production

		app_token = client.Auth.client()

		href = dwolla_get_account_href(app_token)
		funding_resource = dwolla_get_funding_sources(app_token, href)

		data["href"] = href
		data["funding_resource"] = funding_resource

	return render(request, "dwollaTest.html", {'data': data})