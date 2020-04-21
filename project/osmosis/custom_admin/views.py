from django.shortcuts import render
from django.core.management import call_command
from osmosis.payout.models import Payout
from osmosis.payment.models import Payment
from osmosis.app.models import App
from osmosis.account.ledger.models import Ledger
from osmosis.customauth.models import User
from osmosis.inquery.models import Inquery
from django.db.models import Sum
from django.http import HttpResponse
from django.conf import settings

from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas	

import datetime, logging, json
logger = logging.getLogger("django")


def contact_us(request):
	data = {}
	data["success"]=False

	if request.method == 'POST':
		try:
			
			plaintext = get_template('emails/contact_us.txt')
			htmly     = get_template('emails/contact-us.html')
			message = request.POST.get("message")
			name = request.POST.get("name")
			email = request.POST.get("email")
			subject = request.POST.get("subject")

			d = { 'Name': name, 'Email': email, 'Subject': subject, 'Message': message }
			
			subject, from_email, to = subject, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			r = msg.send()

			if r:
				data["success"]=True
				Inquery.objects.create(name=name, subject=subject, email=email, message = message)
		except Exception as e:
			
			data["error"]=True
			data["response"] = e
		
		

	return render(request, "contact-us.html", {'data': data})


def send_test_emails(request):
	data = {}
	data["success"]=False
	if request.method == 'POST':
		try:	
			
			"""
			recipient_list = [request.POST.get("sentTo"),]
			subject = 'Thank you for registering to our site'
			message = ' it  means a world to us '
			email_from = settings.EMAIL_HOST_USER
			recipient_list = ['kirajmd@gmail.com',]
			r = send_mail( subject, message, email_from, recipient_list )
			logger.info(r)
			if r:
				data["success"]=True
		
			"""
			d = { 'username': "New User" }
			#recipient_list = [request.POST.get("recipient"),]

			emailType = request.POST.get("emailType")
			logger.info("emailType")
			logger.info(emailType)
			if emailType == "verify":

				plaintext = get_template('emails/verify.txt')
				htmly     = get_template('emails/verify.html')
				d["link"]="testLink"

			if emailType == "welcome":
				
				plaintext = get_template('emails/welcome_email.txt')
				htmly     = get_template('emails/welcome_email.html')
			
			if emailType == "redeem":
				
				plaintext = get_template('emails/redeemed-cash.txt')
				htmly     = get_template('emails/redeemed-cash.html')

			if emailType == "resetPassword":
				
				plaintext = get_template('emails/reset-password.txt')
				htmly     = get_template('emails/reset-password.html')

			if emailType == "changedSettings":
				
				plaintext = get_template('emails/settings-change.txt')
				htmly     = get_template('emails/settings-change.html')

			if emailType == "changedPassword":
				
				plaintext = get_template('emails/password-change.txt')
				htmly     = get_template('emails/password-change.html')
			

			subject, from_email, to = 'Welcome', settings.EMAIL_HOST_USER, request.POST.get("recipient")
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			r = msg.send()

			logger.info(r)
			if r:
				data["success"]=True
			else:
				data["error"]=True
				data["response"]= "There was an issue"



		except Exception as e:
			
			data["response"] = e
		
		return HttpResponse(json.dumps(data), content_type="application/json")

	return render(request, "admin/send_test_email.html", {'data': data})

def erase_test_data(request):
	data = {}

	if request.method == 'POST':
		try:
			r = call_command('erase_for_testing')
			data["success"]=True
			data["response"] = r
			logger.info(r)
		except Exception as e:
			data["success"]=False
			data["response"] = e
		
		return HttpResponse(json.dumps(data), content_type="application/json")

	return render(request, "admin/erase_test_data.html", {'data': data})


def send_app_report(request):
	data = {}

	data["apps"] = App.objects.all()

	if request.method == 'POST':
		data = {}
		data["success"]=True
		data["response"] = ""
		app_id = request.POST.get("merchant_id")
		app = App.objects.get(pk=app_id)
		data["name"] = app.name
		data["email"] = app.owner.email
		



		res = send_mail("Merchant report test", "Testing", "kira@appevate.com", ["kirajmd@gmail.com"])
		logger.info(res)


		return HttpResponse(json.dumps(data), content_type="application/json")
	
	theBuffer = io.BytesIO()
	p = canvas.Canvas(theBuffer)
	p.drawString(100, 100, "Merchant Report")
	p.showPage()
	p.save()
	theBuffer.seek(0)
	response = FileResponse(theBuffer, content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="hello.pdf"'
	return response

	return render(request, "admin/merchant_report.html", {'data': data})

def run_test(request):
	data = {}


	if request.method == 'POST':
		logger.info("here")
		try:
			testType = request.POST.get("testType")
			if testType == "action_type":
				logger.info("2")
				#call_command('test', 'osmosis.action_type')
				data["success"]=True
				data["response"] = ""
		except Exception as e:
			logger.info(e)
			data["response"] = e

	return HttpResponse(json.dumps("Error"), content_type="application/json")



def admin_payouts(request):
	data = {}

	if request.method == 'POST':
		r = call_command('settle_payouts')
		data["success"]=True
		data["response"] = r

	return render(request, "admin/admin_payouts.html", {'data': data})


def admin_payments(request):
	data = {}

	if request.method == 'POST':
		data["success"]=True

	return render(request, "admin/admin_payouts.html", {'data': data})


def admin_payout_report(request):
	data = {}
	data["payouts"] = Payout.objects.all() 
	data["apps"] = App.objects.all()
	return render(request, "admin/admin_payout_report.html", {'data': data})

def admin_payment_report(request):
	data = {}
	data["payments"] = Payment.objects.all() 
	data["apps"] = App.objects.all()
	data["waitingPayout"] = Ledger.objects.filter(payment__isnull=True, payout__isnull=True)
	return render(request, "admin/admin_payment_report.html", {'data': data})

def admin_user_report(request):
	data = {}
	available = Ledger.objects.filter(payout__isnull=False, payment=None)
	users = Ledger.objects.all().values_list("user", flat=True).distinct()
	data["users"] = User.objects.filter(pk__in=users)
	return render(request, "admin/user_report.html", {'data': data})

def admin_unit_tests(request):
	data = {}
	available = Ledger.objects.filter(payout__isnull=False, payment=None)
	users = Ledger.objects.all().values_list("user", flat=True).distinct()
	data["users"] = User.objects.filter(pk__in=users)
	return render(request, "admin/unit_tests.html", {'data': data})

def admin_revenue_report(request):
	data = {}
	today = datetime.datetime.today()
	year = request.GET.get("year")

	if not year:
		year = today.year
	
	data["apps"] = App.objects.all()

	all_payouts = Ledger.objects.filter(payout__isnull=False)
	data["All_Payouts"] =  all_payouts.aggregate(Sum('amount'))["amount__sum"]
	
	ytd_payouts = all_payouts.filter(**{ "created__year": year})
	data["YTD_Payouts"] = ytd_payouts.aggregate(Sum('amount'))["amount__sum"]

	all_payments = Ledger.objects.filter(payment__isnull=False)
	data["All_Payments"] =  all_payments.aggregate(Sum('amount'))["amount__sum"]
	
	ytd_payments = all_payments.filter(**{ "created__year": year})
	data["YTD_Payments"] = ytd_payments.aggregate(Sum('amount'))["amount__sum"]
	

	return render(request, "admin/revenue_report.html", {'data': data})

def admin_filter_payouts(request):
	data = {}

	
	platform = request.GET.get("platform")
	app = request.GET.get("app")
	if app and app!='all':
		payouts = Payout.objects.filter(app=app)
	else:
		payouts = Payout.objects.all()

	time = request.GET.get("time")
	mData = []
	now = datetime.datetime.now()
	
	if(time=="year"):
			for n in (2017,2018, 2019):
				mPayouts = payouts.filter(**{ "created__year": n})
				mData.append({"header":n, "payouts" : mPayouts})

	
	if(time=="week"):
		headers = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
		for n in range(1,8):
			mPayouts = payouts.filter(**{ "created__week_day": n})
			mData.append({"header":headers[n-1], "payouts" : mPayouts})
			
	
				
	if(time=="month" and time !="all"):
		 
		headers=["Jan", "Feb","Mar","Apr","May","June","July","Aug","Sept","Oct", "Nov", "Dec"]
		

		for n in range(1,13):
			logger.info(n)
			mPayouts = payouts.filter(**{ "created__month": n, "created__year": now.year})
			mData.append({"header":headers[n-1], "payouts" : mPayouts})

	data["payouts"] = payouts
	data["mData"] = mData

	return render(request, "admin/adminPayoutSnippet.html", {'data': data})


def admin_filter_payments(request):
	data = {}
	
	status = request.GET.get("status")

	payments = Payment.objects.all()

	if status and status =="paid":
		payments = Ledger.objects.filter(payment__isnull=False)

	if status and status =="waitPayout":
		payments = Ledger.objects.filter(payout__isnull=True)

	if status and status =="waitPayment":
		payments = Ledger.objects.filter(payment__isnull=True, payout__isnull=False)


	time = request.GET.get("time")
	mData = []
	now = datetime.datetime.now()
	
	if(time=="year"):
			for n in (2017,2018, 2019):
				mPayouts = payments.filter(**{ "created__year": n})
				mData.append({"header":n, "payments" : mPayouts})

	
	if(time=="week"):
		headers = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
		for n in range(1,8):
			mPayouts = payments.filter(**{ "created__week_day": n})
			mData.append({"header":headers[n-1], "payments" : mPayouts})
			
	
				
	if(time=="month" and time !="all"):
		 
		headers=["Jan", "Feb","Mar","Apr","May","June","July","Aug","Sept","Oct", "Nov", "Dec"]
		

		for n in range(1,13):

			mPayouts = payments.filter(**{ "created__month": n, "created__year": now.year})
			mData.append({"header":headers[n-1], "payments" : mPayouts})

	data["payments"] = payments
	data["mData"] = mData

	return render(request, "admin/adminPaymentSnippet.html", {'data': data})