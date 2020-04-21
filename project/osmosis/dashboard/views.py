from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from osmosis.program.models import Program
from osmosis.program.forms import ProgramFormWizard_1, ProgramFormWizard_2, ProgramForm
from osmosis.app.models import App
from osmosis.app.forms import AppForm
from osmosis.event.models import Event
from osmosis.action_type.models import ActionType
from osmosis.action_type.forms import ActionTypeForm
from osmosis.action.models import Action
from osmosis.account.models import Account
from osmosis.account.ledger.models import Ledger
from osmosis.metric.models import Metric
from osmosis.metric.forms import MetricForm
from osmosis.payment.models import Payment
from osmosis.payout.models import Payout as Dashboard_Payout
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


@login_required
def integration_info(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app.id


	return render(request, "dashboard_integration.html", {'data': data})


@login_required
def webhooks(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app_id

	app = apps[0]
	data["app"] = app


	return render(request, "webhooks.html", {'data': data})


@login_required
def user_interface(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app_id
	app = apps[0]


	return render(request, "user-interface.html", {'data': data})

@login_required
def custom_css(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app_id
	app = apps[0]
	data["app"] = app
	url = request.POST.get("css_url")
	f = open('static/css/main.css', 'r')
	file_content = f.read()
	f.close()


	data["css"] = file_content

	if request.method == 'POST':
		app.css_url = url
		app.save()
		data['added']=True
		


	return render(request, "custom-css.html", {'data': data})


@login_required
def sample_templates(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app_id
	app = apps[0]
	data["app"]=app
	added = False

	if request.method == 'POST':
		data["added"] = True
		app.ui_style = request.POST.get("editList")
		logger.info("style %s" % request.POST.get("editList"))
		if request.POST.get("editList") == "3":
			app.custom_color = request.POST.get("themeColor")
		app.save()



	return render(request, "sample-templates.html", {'data': data})

@login_required
def event_tracking(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app_id
	app = apps[0]


	return render(request, "event-tracking.html", {'data': data})

@login_required
def rewards_tracking(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["appId"] = app_id
	app = apps[0]


	return render(request, "rewards-tracking.html", {'data': data})


@login_required
def active_program(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	app = apps[0]
	data["app"] = app
	added = False
	data["appId"] = app_id
	data["program"]= None

	programs = Program.objects.filter(app__pk=app_id, isActive=True)
	data["programs"] = programs
	if programs:
		logger.info(programs[0].name)
		data["program"] = programs[0]

		if request.method == 'POST':
			form = ProgramForm(request.POST, instance = data["program"])
			if form.is_valid():
				logger.info("valid")
				form.save()  
				added = True
			else:
				logger.info("not valid")
				logger.info(form.errors)
	        
	data["added"] = added
	data["form"] = ProgramForm(instance = data["program"])
	return render(request, "active-program.html", {'data': data})

@login_required
def edit_program(request, program_id):

	data = {}
	program = Program.objects.get(pk=program_id)
	app = program.app
	data["app"] = app
	added = False
	data["appId"] = app.id

	data["program"] = program


	if request.method == 'POST':

		if request.POST.get("isActive") and not app.stripe_id:
			data["activeError"] = True
			data["form"] = ProgramForm(instance = data["program"])
			logger.info(program)
			return render(request, "edit-programs.html", {'data': data})
		
		form = ProgramForm(request.POST, instance = program)
		if form.is_valid():
			logger.info("valid")
			form.save()  
			added = True

			cType = request.POST.get("editList")

			if cType and cType == "CPM":
				data["program"].CPM = True
				data["program"].save()
			if cType and cType == "CPC":
				data["program"].CPC = True
				data["program"].save()
			if cType and cType == "CPA":
				data["program"].CPA = True
				data["program"].save()
		else:
			logger.info("not valid")
			logger.info(form.errors)


        
	data["added"] = added 
	data["form"] = ProgramForm(instance = data["program"])


	

	return render(request, "edit-programs.html", {'data': data})

@login_required
def inactive_programs(request, app_id):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps

	app = apps[0]
	data["appId"] = app_id

	data["programs"] = Program.objects.filter(app__pk=app_id, isActive=False)



	return render(request, "inactive-programs.html", {'data': data})



@login_required
def create_program_1(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	app = apps[0]
	data["app"] = app
	data["appId"] = app.id
	
	added = False
	cType = request.session.get("cType", None)
	
	if request.method == 'POST':
		form = ProgramFormWizard_1(request.POST)

		if form.is_valid():
			logger.info("is valid")
			#form.save()  
			request.session["name"]=form.cleaned_data["name"]
			request.session["description"]=form.cleaned_data["description"]
			request.session["cType"]=request.POST.get("editList")
			
			
			#redirect to 2
			return redirect('create_program_2')
		else:
			logger.info("not valid")
			logger.info(form.errors)

	name = request.session.get("name", None) 
	description = request.session.get("description", None)
	data["description"]=description
	data["cType"]= cType
	data["form"] = ProgramFormWizard_1(initial={"app":app.id, 'name': name, 'description':description})
	

	#logger.info("" % data["form"])
	

	data["added"] = added 
	return render(request, "create-program.html", {'data': data})

@login_required
def create_program_2(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	app = apps[0]
	data["app"] = app
	data["appId"] = app.id
	
	added = False

	if request.method == 'POST':
		form = ProgramFormWizard_2(request.POST)

		if form.is_valid():
			logger.info("is valid")
			request.session["budget"]=request.POST.get("budget")
			
			#redirect to 2
			return redirect('create_program_3')
		else:
			logger.info("not valid")
			logger.info(form.errors)

	budget = request.session.get("budget")

	data["form"] = ProgramFormWizard_2(initial={"app":app.id, "budget":budget})
	return render(request, "create-program2.html", {'data': data})

@login_required
def create_program_3(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	app = apps[0]
	data["app"] = app
	data["appId"] = app.id
	
	added = False

	if request.method == 'POST':
		form = ProgramForm(request.POST)

		if form.is_valid():
			logger.info("is valid")
			cType = request.session["cType"]
			if cType=="CPA":
				form.CPA = True
			if cType=="CPM":
				form.CPM = True
				#form.cleaned_data["CPM"] = True
				logger.info("CPM")
			if cType=="CPC":
				form.CPC = True

			form.save()  
			request.session["name"] = None
			request.session["budget"] = None
			request.session["description"] = None
			request.session["cType"]=None
			
			#redirect to 2
			added=True
		else:
			logger.info("not valid")
			logger.info(form.errors)
			#logger.info(form)

	data["budget"] = request.session.get("budget")
	data["name"] = request.session.get("name")
	data["description"] = request.session.get("description")
	data["cType"] = request.session.get("cType")        
	data["form"] = ProgramForm(initial={"app":app.id, "name":data["name"], "budget":data["budget"], "description":data["description"]})
	data["added"] = added 
	return render(request, "create-programSummary.html", {'data': data})



@login_required
def delete_program(request, program_id):

	data = {}
	program = Program.objects.get(pk=program_id)
	app = program.app
	data["app"] = app
	added = False
	data["appId"] = app.id

	data["program"] = program
	data["ledgers"] = Ledger.objects.filter(action__action_type__program=program) 

	if request.method == 'POST':
		if data["ledgers"] or program.isActive:
			pass
			#don't delete
			logger.info("don't delete")

		else:
			logger.info("delete program")
			#program.delete()
			data["deleted"] = True
        
	data["added"] = added 
	data["form"] = ProgramForm(instance = data["program"])
	
	
	

	return render(request, "delete-program.html", {'data': data})


@login_required
def dashboard_settings(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	
	logger.info("settings")
	app = apps[0]
	data["appId"] = app.id
	data["app"]=app

	if request.method == 'POST':
		logger.info("post")
		logger.info(request.POST)
		logger.info("id: %s" % request.POST.get("stripe_id"))
		app.stripe_id = request.POST.get("stripe_id")
		app.stripe_account = request.POST.get("stripe_account")
		app.save()
		data["added"]=True
		
		"""
		form = AppForm(request.POST, instance=app)
		logger.info(form)
		logger.info(request.POST)
		if form.is_valid():
			form.save()  
			data["added"] = True
			logger.info("valid")
		else:
			logger.info("else")
			pass
		"""

	data["form"] = AppForm(instance=app)
	#logger.info(data["form"])

	return render(request, "payment-settings.html", {'data': data})


@login_required
def app_profile(request):

	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	

	app = apps[0]
	data["appId"] = app.id
	data["app"]=app

	if request.method == 'POST':
		form = AppForm(request.POST, instance=app)
		logger.info(form)
		logger.info(request.POST)
		if form.is_valid():
			form.save()  
			data["added"] = True
			logger.info("valid")
		else:
			#logger.info("else")
			pass

	data["form"] = AppForm(instance=app)
	#logger.info(data["form"])

	return render(request, "settings.html", {'data': data})


@login_required
def dashboard_main(request):
	logger.info("d")
	data = {}
	apps = App.objects.filter(owner__user=request.user)
	data["apps"] = apps
	data["app"] = apps[0]

	app = apps[0]
	data["appId"] = app.id
	data["stripe"] =  app.stripe_id

	if request.method == 'POST':
		logger.info("post")
		logger.info(request.POST)
		logger.info("id: %s" % request.POST.get("stripe_id"))
		app.stripe_id = request.POST.get("stripe_id")
		app.stripe_account = request.POST.get("stripe_account")
		app.save()
		data["added"]=True
		data["app"] = app
		data["stripe"] =  app.stripe_id



	return render(request, "dashboard.html", {'data': data})
"""
@login_required
def delete_program(request, program_id):
	data = {}
	added = False
	program = Program.objects.get(pk=program_id)
	#program.delete()

	return redirect('/app-detail/'+str(program.app.id) + "/")
"""

@login_required
def delete_metric(request, metric_id):
	data = {}
	added = False
	metric = Metric.objects.get(pk=metric_id)
	metric.delete()

	return redirect('/custom-metrics/'+str(metric.program.id) + "/")

@login_required
def delete_action_type(request, action_type_id):
	data = {}
	added = False
	at = ActionType.objects.get(pk=action_type_id)
	at.delete()

	return redirect('/app-detail/'+str(at.app.id) + "/")

@login_required
def delete_app(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	app.delete()

	return redirect('/dashboard/')

@login_required
def change_card(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	customer = None
	stripe.api_key = settings.STRIPE_SECRET_KEY
	
	if app.owner.user != request.user:
		return redirect('/dashboard/')

	if app.stripe_id:
		customer = stripe.Customer.retrieve(app.stripe_id)

@login_required
def dashboard_payments(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	data["app"] = app
	
	if app.owner.user != request.user:
		return redirect('/dashboard/')

	
	data["payments"] = Payment.objects.all()
	
	return render(request, "payments.html", {'data': data})


@login_required
def dashboard_payouts(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	data["app"] = app
	
	#if app.owner.user != request.user:
	#	return redirect('/dashboard/')

	data["payouts"] = Dashboard_Payout.objects.filter(app = app )
	logger.info(data["payouts"])
	
	return render(request, "dashboard_payouts.html", {'data': data})

@login_required
def dashboard_filter_payouts(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	data["app"] = app
	
	#if app.owner.user != request.user:
	#	return redirect('/dashboard/')

	data["payouts"] = Payout.objects.filter(account__program__app = app )
	
	return render(request, "dashboard_payouts.html", {'data': data})


@login_required
def payouts(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	customer = None
	stripe.api_key = settings.STRIPE_SECRET_KEY
	data ["stripe_key"] = settings.STRIPE_TEST_PUBLIC_KEY
	
	if app.owner.user != request.user:
		return redirect('/dashboard/')

	if app.stripe_id:
		customer = stripe.Customer.retrieve(app.stripe_id)

	if customer:
		logger.info(customer)
		data["last4"] = customer.sources.data[0].last4
	
	if request.method == 'POST':
		
		if customer:
			customer = stripe.Customer.modify(
		  		customer.id,
		  		source=request.POST.get("stripeToken"),
			)
		else:

			customer = stripe.Customer.create(
			    source=request.POST.get("stripeToken"),
			    email=app.owner.email,

			)
		data["customer"]=customer
		data["last4"] = customer.sources.data[0].last4
		app.stripe_id = customer.id
		app.save()
		#logger.info(customer)
		added = True  

	'''#new card to customer
			customer = stripe.Customer.create_source(
	  'cus_AFGbOSiITuJVDs',
	  source='src_18eYalAHEMiOZZp1l9ZTjSU0'
	)
	'''
	data["app"] = app
	data["added"] = added 


	return render(request, "payouts.html", {'data': data})

@login_required
def stripe_charge(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	logger.info(request)
	logger.info("here")
	data["req"] = request.POST
	#is this app id owned by user?
	stripe.api_key = settings.STRIPE_SECRET_KEY
	if request.method == 'POST':
		customer = stripe.Customer.create(
		    source=request.POST.get("stripeToken"),
		    email='paying3.user@example.com',

		)
		logger.info(customer)
	        
	data["app"] = app
	data["added"] = added 
	
	#data["form"] = ProgramForm(initial={"app":app.id})

	return render(request, "payouts.html", {'data': data})

@login_required
def app_info(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)

	if request.method == 'POST':
		form = ProgramForm(request.POST)
		if form.is_valid():
			form.save()  
			added = True
	        
	data["app"] = app
	data["programs"] = Program.objects.filter(app=app)
	data["form"] = ProgramForm(initial={"app":app.id})
	data["actionTypes"] = ActionType.objects.filter(app=app)
	data["added"] = added 
	
	
	return render(request, "app-detail.html", {'data': data})

@login_required
def program_info(request, program_id):
	data = {}
	added = False
	program = Program.objects.get(pk=program_id)
	logger.info("here")
	if request.method == 'POST':
		form = ProgramForm(request.POST, instance=program)
		if form.is_valid():
			form.save()  
			added = True

	
	data["program"] = program
	data["form"] = ProgramForm(instance=program)
	data["added"] = added 
	#data["metrics"] = Metric.objects.filter(program=program) 

	return render(request, "programDetail.html", {'data': data})

@login_required
def custom_metrics(request, program_id):
	data = {}
	added = False
	data["program"] = Program.objects.get(pk=program_id)

	if request.method == 'POST':
		logger.info("post")
		form = MetricForm(request.POST)
		if form.is_valid():
			logger.info("valid")
			form.save()  
			added = True
		else:
			data["form"] = form
			return render(request, "custom-metrics.html", {'data': data})
	        
	data["metrics"] = Metric.objects.filter(program=data["program"]) 
	data["form"] = MetricForm(initial={"program_id":program_id})
	data["added"] = added 


	return render(request, "custom-metrics.html", {'data': data})


@login_required
def edit_metric(request, metric_id):
	data = {}
	added = False
	metric = Metric.objects.get(pk=metric_id)
	

	if request.method == 'POST':
		form = MetricForm(request.POST, instance = metric)
		if form.is_valid():
			form.save()  
			added = True
		else:
			data["form"] = form
			return render(request, "edit_metric.html", {'data': data})        
	
	data["form"] = MetricForm(instance=metric)
	data["added"] = added 
	data["metric"] = metric

	return render(request, "edit-metric.html", {'data': data})	

@login_required
def edit_app(request, app_id):
	data = {}
	added = False
	app = App.objects.get(pk=app_id)
	

	if request.method == 'POST':
		form = AppForm(request.POST, instance = app)
		if form.is_valid():
			form.save()  
			added = True
		else:
			data["form"] = form
			return render(request, "edit_app.html", {'data': data})        
	
	data["form"] = AppForm(instance=app)
	data["added"] = added 
	data["app"] = app

	return render(request, "edit-app.html", {'data': data})


@login_required
def edit_action_type(request, action_type_id):
	data = {}
	added = False
	at= ActionType.objects.get(pk=action_type_id)
	

	if request.method == 'POST':
		form = ActionTypeForm(request.POST, instance = at)
		if form.is_valid():
			form.save()  
			added = True
		else:
			data["form"] = form
			return render(request, "edit-action-type.html", {'data': data})        
	
	data["form"] = ActionTypeForm(instance=at)
	data["added"] = added 
	data["action_type"] = at


	return render(request, "edit-action-type.html", {'data': data})	

@login_required
def program_metrics_detail(request, program_id):
	data = {}

	program = Program.objects.get(pk=program_id)
	data["program"] = program
	data["metricData"] = []
	metrics =  Metric.objects.filter(program=program) 
	#actionTypes = ActionType.objects.filter(app = program.app)
	data["events"] = Event.objects.filter(program = program)
	
	for metric in metrics:
		mData ={}
		mData["name"] = metric.name
		actionsFirst = Action.objects.filter(program=program, action_type=metric.first)
		actionsSecond = Action.objects.filter(program=program, action_type=metric.second)
		mData["first"] = []
		mData["second"] = []
		mData["headers"] = []

		for n in (2017,2018):
			aF = actionsFirst.filter(**{ "created__year": n})
			aS = actionsSecond.filter(**{ "created__year": n})
			mData["first"].append(aF.count())
			mData["second"].append(aS.count())
			mData["headers"].append(n)

		data["metricData"].append(mData)
	
	return render(request, "programMetricDetail.html", {'data': data})	

@login_required
def user_metrics_detail(request, program_id, user_id):
	data = {}
	user = User.objects.get(pk=user_id)
	data["user"] = user
	program = Program.objects.get(pk=program_id)
	data["program"] = program
	data["metricData"] = []
	metrics =  Metric.objects.filter(program=program) 
	#actionTypes = ActionType.objects.filter(app = program.app)
	data["events"] = Event.objects.filter(program = program)
	
	for metric in metrics:
		mData ={}
		mData["name"] = metric.name
		actionsFirst = Action.objects.filter(program=program, action_type=metric.first, fromUser=user)
		actionsSecond = Action.objects.filter(program=program, action_type=metric.second, fromUser = user)
		mData["first"] = []
		mData["second"] = []
		mData["headers"] = []

		for n in (2017,2018):
			aF = actionsFirst.filter(**{ "created__year": n})
			aS = actionsSecond.filter(**{ "created__year": n})
			mData["first"].append(aF.count())
			mData["second"].append(aS.count())
			mData["headers"].append(n)

		data["metricData"].append(mData)
		
	
	return render(request, "userMetricDetail.html", {'data': data})


@login_required
def filterMetrics(request):
	data = {}
	respData = {}
	respData["html"] = ""
	respData["success"] = True
	filterType  = request.POST.get("type")

	program_id = request.POST.get("program_id")
	program = Program.objects.get(pk=program_id)
	metrics =  Metric.objects.filter(program=program) 
	
	data["program"] = program
	data["metricData"] = []
	
	#actionTypes = ActionType.objects.filter(app = program.app)
	
	time = request.POST.get("time")
	data["time"] = time
	event_id = request.POST.get("value")
	
	for metric in metrics:
		mData ={}
		mData["name"] = metric.name
		
		actionsFirst = Action.objects.filter(program=program, action_type=metric.first)
		actionsSecond = Action.objects.filter(program=program, action_type=metric.second)

		if(filterType=="event"):
			event = Event.objects.get(pk=event_id)
			actionsFirst = actionsFirst.filter(event=event)
			actionsSecond = actionsSecond.filter(event=event)
		
		mData["first"] = []
		mData["second"] = []
		mData["headers"] = []
		if(time=="year"):
			for n in (2017,2018):
				aF = actionsFirst.filter(**{ "created__year": n})
				aS = actionsSecond.filter(**{ "created__year": n})
				mData["first"].append(aF.count())
				mData["second"].append(aS.count())
				mData["headers"].append(n)

		
		if(time=="week"):
			mData["headers"] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			for n in range(0,7):
				aF = actionsFirst.filter(**{ "created__week_day": n})
				aS = actionsSecond.filter(**{ "created__week_day": n})
				mData["first"].append(aF.count())
				mData["second"].append(aS.count())
				
		if(time=="month"):
		 
			mData["headers"]=["Jan", "Feb","Mar","Apr","May","June","July","Aug","Sept","Oct", "Nov", "Dec"]
			now = datetime.datetime.now()

			for n in range(0,12):
				aF = actionsFirst.filter(**{ "created__month": n, "created__year": now.year})
				aS = actionsSecond.filter(**{ "created__month": n, "created__year": now.year})
				mData["first"].append(aF.count())
				mData["second"].append(aS.count())


		

		data["metricData"].append(mData)
	
	respData["html"] = render_to_string("programMetricSnippet.html", {'data': data})
	return HttpResponse(json.dumps(respData), content_type="application/json")


@login_required
def programs_by_app(request, app_id):
	data = {}
	app = App.objects.filter(pk=app_id)
	data["app"] = app
	data["programs"] = Program.objects.filter(app=app)


	return render(request, "programs.html", {'data': data})

@login_required
def ledgers_by_payment(request, payment_id):
	data = {}
	data["payment"] = Payment.objects.get(pk=payment_id)
	ledgers = Ledger.objects.filter(payment = data['payment'])
	data["ledgers"] = ledgers
	


	return render(request, "ledgers_by_payment.html", {'data': data})


def dashboard_filter_payments(request, app_id):
	data = {}
	app = App.objects.filter(pk=app_id)
	data["app"] = app
	payments = Payment.objects.filter(account__program__app = app )
	platform = request.GET.get("platform")
	time = request.GET.get("time")
	mData = []
	now = datetime.datetime.now()
	if platform and platform != "all":
		payments = payments.filter(platform = platform)
	
	
	if(time=="year"):
			for n in (2017,2018, 2019):
				mPayments = payments.filter(**{ "created__year": n})
				mData.append({"header":n, "payments" : mPayments})

	
	if(time=="week"):
		headers = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
		for n in range(1,8):
			mPayments = payments.filter(**{ "created__week_day": n})
			mData.append({"header":headers[n-1], "payments" : mPayments})
			
	
				
	if(time=="month" and time !="all"):
		 
		headers=["Jan", "Feb","Mar","Apr","May","June","July","Aug","Sept","Oct", "Nov", "Dec"]
		

		for n in range(1,13):
			logger.info(n)
			mPayments = payments.filter(**{ "created__month": n, "created__year": now.year})
			mData.append({"header":headers[n-1], "payments" : mPayments})

	data["payments"] = payments
	data["mData"] = mData

	return render(request, "paymentSnippet.html", {'data': data})


def webframe_dashboard(request, user_id):
	data = {}
	
	try:
		
		#tokenStr = str(request.META.get('HTTP_AUTHORIZATION').split()[1])
		#token = Token.objects.get(key = tokenStr)
		app_id = request.GET.get("app_id", 1)
		app = App.objects.get(pk = app_id)
		data["app"] = app
		redeemed = False
		data["balance"] = 0
		user = User.objects.get(pk=user_id)
		data["user"] = user
		data["css_url"] = request.GET.get("css_url")
		logger.info(request.GET.get("css_url"))
		#data["welcome_message"] = config.WELCOME_MESSAGE

		if not user.paypal_email and request.method != 'POST' :
			return render(request, "webframe/blurb.html", {'data': data})

		accounts = Account.objects.filter(user=user_id)
		if len(accounts) < 1:
			balance = 0
		else:
			balance = accounts[0].balance
		
		ledgers = Ledger.objects.filter(user=user)
		available = Ledger.objects.filter(user=user, payout__isnull=False, payment=None)
		total =  Ledger.objects.filter(user=user, payment=None)
		data["available"] = available.aggregate(Sum('amount'))["amount__sum"]

		if not data["available"]:
			data["available"] = 0

		data["total"] = total.aggregate(Sum('amount'))["amount__sum"]

		if not data["total"]:
			data["total"] = 0

		if request.method == 'POST':
			if request.POST.get("paypal-email", None):
				user.paypal_email = request.POST.get("paypal-email")
				user.save()

	
		data["user_id"] = user_id 
		data["redeemed"] = redeemed
		

		return render(request, "webframe/dashboard.html", {'data': data})
	except Exception as e:
		logger.info(e)
		return HttpResponse(500)

def webframe_dashboard_template(request, style):
	data = {}
	
	try:
		user_id = 1
		#tokenStr = str(request.META.get('HTTP_AUTHORIZATION').split()[1])
		#token = Token.objects.get(key = tokenStr)
		app_id = request.GET.get("app_id", 1)
		app = App.objects.get(pk = app_id)
		data["app"] = app
		redeemed = False
		data["balance"] = 0
		user = User.objects.get(pk=user_id)
		data["user"] = user
		data["sample"] = True
		data["style"] = style
		#data["welcome_message"] = config.WELCOME_MESSAGE

		if not user.paypal_email and request.method != 'POST' :
			return render(request, "webframe/blurb.html", {'data': data})

		accounts = Account.objects.filter(user=user_id)
		if len(accounts) < 1:
			balance = 0
		else:
			balance = accounts[0].balance
		
		ledgers = Ledger.objects.filter(user=user)
		available = Ledger.objects.filter(user=user, payout__isnull=False, payment=None)
		total =  Ledger.objects.filter(user=user, payment=None)
		data["available"] = available.aggregate(Sum('amount'))["amount__sum"]

		if not data["available"]:
			data["available"] = 0

		data["total"] = total.aggregate(Sum('amount'))["amount__sum"]

		if not data["total"]:
			data["total"] = 0

		if request.method == 'POST':
			if request.POST.get("paypal-email", None):
				user.paypal_email = request.POST.get("paypal-email")
				user.save()

	
		data["user_id"] = user_id 
		data["redeemed"] = redeemed
		

		return render(request, "webframe/dashboard.html", {'data': data})
	except Exception as e:
		logger.info(e)
		return HttpResponse(500)


def webframe_active_program_detail(request):
	try:
		#tokenStr = str(request.META.get('HTTP_AUTHORIZATION').split()[1])
		#token = Token.objects.get(key = tokenStr)
		api_key = request.GET.get("api_key")
		#app = App.objects.filter(api_key=api_key, owner__user = token.user)
		app= App.objects.filter(api_key=api_key)
		if len(app) < 1:
			return HttpResponse(status=500)
		program = Program.objects.filter(app=app[0], isActive = True)
		data = {}
		
		if len(program) > 0:
			data["program"] = program[0]	
			data["actionTypes"] = ActionType.objects.filter(program = program[0].id)
		return render(request, "webframe/activeProgramDetail.html", {'data': data})
	except Exception as e:
		return HttpResponse(500)


def webframe_user_form(request, user_id):
	data = {}

	try:
		#tokenStr = str(request.META.get('HTTP_AUTHORIZATION').split()[1])
		#token = Token.objects.get(key = tokenStr)
		user = User.objects.get(pk=user_id)
		data["user"] = user
	
		
		if request.method == 'POST':
			if request.POST.get("phone"):
				user.phone_number = request.POST.get("phone")
			if request.POST.get("venmo_email"):
				user.venmo_email = request.POST.get("venmo_email")
			if request.POST.get("paypal_email"):
				user.paypal_email = request.POST.get("paypal_email")
			logger.info("saving")
			
			user.save()
			
			return HttpResponse(json.dumps({"success":True}), content_type="application/json")

		return render(request, "webframe/form.html", {'data': data})
	except Exception as e:
		return HttpResponse(e)



def user_dashboard(request, user_id):
	data = {}
	user = User.objects.get(pk=user_id)
	data ["user"] = user
	return render(request, "user/dashboard.html", {'data': data})

def user_payments(request, user_id):
	data = {}
	user = User.objects.get(pk=user_id)
	data ["user"] = user
	data["ledgers"] = Ledger.objects.filter(user = user, payment__isnull=False)
	payment_list = data["ledgers"].values_list("payment", flat=True)
	payments = Payment.objects.filter(id__in = payment_list)
	data["payments"] = []
	for payment in payments:

		leds = Ledger.objects.filter(user = user, payment = payment)
		#data["payments"][payment.id]["ledgers"] = leds
		total = leds.aggregate(Sum('amount'))["amount__sum"]
		data["payments"].append({"ledgers":leds, "id":payment.id, "total" : total, "payments":payment}) 

	#payments = Payment.objects.filter(payment__user = user)
	#data["payments"] = payments
	return render(request, "user/payments.html", {'data': data})

def user_rewards(request, user_id):
	data = {}
	user = User.objects.get(pk=user_id)
	data ["user"] = user
	data["ledgers"] = Ledger.objects.filter(user = user)
	return render(request, "user/rewards.html", {'data': data})





