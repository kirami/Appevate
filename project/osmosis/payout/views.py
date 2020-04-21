from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from osmosis.app.models import App
from osmosis.account.models import Account
from .models import Payment

import paypalrestsdk,datetime

from paypalrestsdk import Payout, ResourceNotFound

import logging, json, requests, md5, urllib2, urllib
logger = logging.getLogger("django")


def stripe_payout_api(request):
	data = {}

	try:
		

	except Exception as e:
		logger.info(e)
		data["success"] = False
		data["message"] = ("There was a problem. % s" % e)

	return HttpResponse(json.dumps(data), content_type="application/json")

