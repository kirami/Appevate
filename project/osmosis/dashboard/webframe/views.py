from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required

from osmosis.customauth.models import User
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.authtoken.models import Token
import stripe
from decimal import Decimal

from django.urls import reverse
import datetime
from django.utils.timezone import now

import paypalrestsdk 

from paypalrestsdk import Payout, ResourceNotFound
from constance import config


# Create your views here.
import logging, json, requests
logger = logging.getLogger("django")
r_logger = logging.getLogger("rangle")
o_logger = logging.getLogger(__name__)


@login_required
def edit_password(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	app = apps[0]
	data["appId"] = app.id

	if request.method == 'POST':
		respData = {}
		user = request.user
		#does the currwnt pw match?

		#change
		user.set_password(request.POST.get("new_password"))
		user.save()
		respData["success"]= True
		return HttpResponse(json.dumps({"success":True}), content_type="application/json")



	return render(request, "edit-password.html", {'data': data})

