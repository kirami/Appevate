from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from osmosis.app.models import App
from osmosis.account.models import Account
from osmosis.account.ledger.models import Ledger
from osmosis.customauth.models import User
from .models import Payment
from osmosis.utils import encrypt_val, decrypt_val
from django.db.models import Sum

import paypalrestsdk,datetime
from django.contrib.admin.views.decorators import staff_member_required

from paypalrestsdk import Payout, ResourceNotFound

# Create your views here.
import logging, json, requests, urllib
from hashlib import md5
logger = logging.getLogger("django")

p_logger = logging.getLogger("payments")


@staff_member_required
def admin_pay(request):
	data = {}
	try:
		user_id = request.POST.get("user_id")
		data = pay(user_id)
	except Exception as e:
		logger.info(e)
	
	return HttpResponse(json.dumps(data), content_type="application/json", status=200)

def pay(user_id):
	data = {}
	try:
		user = User.objects.get(pk=user_id)
		#account = Account.objects.get(user = user_id)
		available = Ledger.objects.filter(user=user_id, payout__isnull=False, payment=None)
		balance = user.get_redeemable
		
		if not user.paypal_email:
			data["success"] = False
			data["message"] = ("You do not have a paypal email setup")
			return data

		if balance > 0:

			my_api = paypalrestsdk.Api({
			'mode': 'sandbox',
			'client_id': settings.PAYPAL_CLIENT_ID,
			'client_secret': settings.PAYPAL_CLIENT_SECRET})
			access_token = my_api.get_access_token()	

			item ={
				"recipient_type": "EMAIL",
				"amount": {
				"value": str(balance),
				"currency": "USD"
			},
				"receiver": user.paypal_email,
				"note": "Thank you.",
				"sender_item_id": "item_1" 
			}

			payout = Payout({
				"sender_batch_header": {
				"sender_batch_id": "batch_" + user_id + str(datetime.datetime.now()),
				"email_subject": "You have a payment"
			},


				"items": [item]
			}, api=my_api)

			p_logger.info("sending: %s" % item )

			if payout.create(sync_mode=False):
				data["success"] = True
				
				p_logger.info("returned: %s" % payout)
				#add payment history in log
				pay = Payment.objects.create(amount = balance, platform="PayPal")
				available.update(payment = pay)
				data["message"] = "Your payment was successful, payment id: " + str(pay.id)
				#zero out account
				#account.balance = 0
				#account.save()
				total =  Ledger.objects.filter(user=user_id, payment=None)
				totalMon = total.aggregate(Sum('amount'))["amount__sum"]
				if not totalMon:
					data["total"] = "0"
				else:
					data["total"] =  str(totalMon)
				data["paidAmount"] = str(balance)
			else:
				data["success"] = False
				data["message"] = "Payment failed."
		else:
			data["success"] = False
			data["message"] = ("You have no available rewards to redeem")
	except Exception as e:
		logger.info("error")
		logger.info(e)
		data["success"] = False
		data["message"] = e.message
		#pass
	return data


def paypal_payment_api(request):
	data = {}

	try:
		key = request.GET.get("api_key")
		logger.info(request.GET)
		secret = request.GET.get("api_secret")
		logger.info("secret %s" % secret)
		user_id = request.GET.get("user_id")
		#logger.info("here id: %s" % request)
		app = App.objects.get(api_key = key)
		user = User.objects.get(pk=user_id)
		"""
		if app:
			app = app[0]
		"""
		logger.info("app key: %s" % app.api_secret )
		#it sends encoded alreadyhere

		if not app.api_secret == secret:
			logger.info("here")
			data["success"] = False
			data["message"] = "Authentication failed."
			return HttpResponse(json.dumps(data), content_type="application/json")
		#user = User.objects.get(pk=user_id)
		#account = Account.objects.get(user = user_id)
		available = Ledger.objects.filter(user=user_id, payout__isnull=False, payment=None)
		balance = available.aggregate(Sum('amount'))["amount__sum"]
		if not user.paypal_email:
			data["success"] = False
			data["message"] = ("You do not have a paypal email setup")

			return HttpResponse(json.dumps(data), content_type="application/json")

		if balance > 0:

			my_api = paypalrestsdk.Api({
			'mode': 'sandbox',
			'client_id': settings.PAYPAL_CLIENT_ID,
			'client_secret': settings.PAYPAL_CLIENT_SECRET})
			access_token = my_api.get_access_token()	

			item ={
				"recipient_type": "EMAIL",
				"amount": {
				"value": str(balance),
				"currency": "USD"
			},
				"receiver": user.paypal_email,
				"note": "Thank you.",
				"sender_item_id": "item_1" 
			}

			payout = Payout({
				"sender_batch_header": {
				"sender_batch_id": "batch_" + user_id + str(datetime.datetime.now()),
				"email_subject": "You have a payment"
			},


				"items": [item]
			}, api=my_api)

			p_logger.info("sending: %s" % item )

			if payout.create(sync_mode=False):
				data["success"] = True
				
				p_logger.info("returned: %s" % payout)
				#add payment history in log
				pay = Payment.objects.create(amount = balance, platform="PayPal")
				available.update(payment = pay)
				data["message"] = "Your payment was successful, payment id: " + str(pay.id)
				#zero out account
				#account.balance = 0
				#account.save()
				total =  Ledger.objects.filter(user=user_id, payment=None)
				totalMon = total.aggregate(Sum('amount'))["amount__sum"]
				if not totalMon:
					data["total"] = "0"
				else:
					data["total"] =  str(totalMon)
				data["paidAmount"] = str(balance)
			else:
				data["success"] = False
				data["message"] = "Payment failed."
		else:
			data["success"] = False
			data["message"] = ("You have no available rewards to redeem")

	except Exception as e:
		logger.info(e)
		data["success"] = False
		data["message"] = ("There was a problem. % s" % e)

	return HttpResponse(json.dumps(data), content_type="application/json")


def batch_pay(payList):

	items = []
	i = 0
	data = {}
	data["success"] = False

	my_api = paypalrestsdk.Api({
			'mode': 'sandbox',
			'client_id': settings.PAYPAL_CLIENT_ID,
			'client_secret': settings.PAYPAL_CLIENT_SECRET})
	access_token = my_api.get_access_token()
	batch = str(datetime.datetime.now())

	for pay_item in payList:
		item ={
			"recipient_type": "EMAIL",
			"amount": {
				"value": str(pay_item["amount"]),
				"currency": "USD"
			},
			"receiver": pay_item["email"],
			"note": "Thank you.",
			"sender_item_id": "item_" + str(i)
		}
		items.append(item)
		i = i + 1
	
	payout = Payout({
		"sender_batch_header": {
		"sender_batch_id": "batch_" + batch,
		"email_subject": "You have a payment"
		},
		

		"items": items
	}, api=my_api)

	if payout.create(sync_mode=False):
		data["successMsg"] = "You've successfully sent a payout, batch id: " + payout.batch_header.payout_batch_id
		data["success"] = True
		data["batch_id"]  =payout.batch_header.payout_batch_id
	else:
		logger.info(payout.error)
		data["message"] = payout.error
	return data

@login_required
def paypal_payment(request):
	data = {}
	logger.info("pp")
	if request.method == "POST":
		try:
			
			my_api = paypalrestsdk.Api({
				'mode': 'sandbox',
				'client_id': settings.PAYPAL_CLIENT_ID,
				'client_secret': settings.PAYPAL_CLIENT_SECRET})

			access_token = my_api.get_access_token()
			#logger.info("token %s" % access_token)
			
			batchId = request.POST.get("batchId")

			if batchId:
				resp = Payout.find(batchId, my_api)
				data["successMsg"] = resp["items"]

			else:
				emails = request.POST.get("email").split(',')
				amounts = request.POST.get("amount").split(',')
				items = []
				i = 0
				for email in emails:
					item ={
						"recipient_type": "EMAIL",
						"amount": {
							"value": amounts[i],
							"currency": "USD"
						},
						"receiver": email,
						"note": "Thank you.",
						"sender_item_id": "item_" + str(i)
					}
					items.append(item)
					i = i + 1
				
				payout = Payout({
					"sender_batch_header": {
					"sender_batch_id": "batch_2",
					"email_subject": "You have a payment"
					},
					

					"items": items
				}, api=my_api)

				if payout.create(sync_mode=False):
					data["successMsg"] = "You've successfully sent a payout, batch id: " + payout.batch_header.payout_batch_id
				else:
					logger.info(payout.error)
					data["message"] = payout.error
		except Exception as e:
			logger.info(e)
			data["message"] =	"Something went wrong."

	return render(request, "paypalTest.html", {'data': data})



class PayPalResponse(object):
	_attrs = {}

	def __init__(self, nvp, unique_id):
		for token in nvp.split('&'):
			self._attrs[token.split("=")[0]] = token.split("=")[1]
		self._attrs['unique_id'] = unique_id
		self._attrs['text'] = nvp

	def __dict__(self):
		return self._attrs

	def __getattr__(self, key):
		return self._attrs[key]
