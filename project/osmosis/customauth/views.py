from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from .forms import ProfileForm, ImageUploadForm
from osmosis.app.models import App
from .models import User
from django.conf import settings



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

import logging, json, random, string
logger = logging.getLogger("django")

@login_required
def ProfileView(request, success=False):
	data = {}
	if request.method == "POST":
		try:
			form = ProfileForm(request.POST, instance = request.user)
			if form.is_valid():
				model_instance = form.save(commit=False)
				#model_instance.timestamp = timezone.now()
				model_instance.save()
				return render(request, "profile.html", {'form': form, "success": True})
			else:
				return render(request, "profile.html", {'form': form})

		except Exception as e:
			logger.info(e)
 
	else:
 
		form = ProfileForm(instance = request.user)
		#owner = Owner.obje
		data["apps"] = App.objects.filter(owner__user=request.user)
 
		return render(request, "profile.html", {'form': form, "data":data, "success": success})


@login_required
def Change_CSS_URL(request):
	data = {}
	
	try:
		logger.info( request.POST)
		logger.info("appid %s " %  request.POST.get("app_id"))
		app = App.objects.filter(owner__user=request.user, pk = request.POST.get("app_id"))[0]
		app.css_url = request.POST.get("css_url")
		app.self_payout = request.POST.get("self_payout", False)
		app.save()

		return HttpResponse(json.dumps({"success":True, "app_id":app.id}), content_type="application/json")
	except Exception as e:
		logger.info(e)
		return HttpResponse(json.dumps({"success":False,  "app_id":app.id}), content_type="application/json")

 
@login_required
def Image_Upload(request):
	data = {}

	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			m = App.objects.get(pk=request.POST.get("app_id"))
			m.image = form.cleaned_data['image']
			m.save()

			return render(request, "profile.html", {'form': form, "success": True})
		else:
			return render(request, "profile.html", {'form': form})

def verifyEmail(request):
	data = {}
	data["success"] = False
	email = request.GET.get("email")
	code = request.GET.get("code")
	try:
		us= User.objects.filter(email=email)
		u = us[0]
		logger.info("verify_code: %s" % u.verify_code)
		if u.verify_code == code:
			data["success"] = True
			u.verified = True
			u.save()
	except Exception as e:
		logger.info(e)
		pass
	return render(request, "verifyEmail.html", {'data': data})

def resetEmail(request):
	data = {}
	
	email = request.POST.get("email")
	if request.method == 'POST':
		data["success"] = True #always say true for security
		try:
			users = User.objects.filter(email=email)
			logger.info("users")
			if users:
				temp  = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
				users[0].set_password(temp)
				users[0].save()
				data["email"] = email

				plaintext = get_template('emails/reset-password.txt')
				htmly     = get_template('emails/reset-password.html')
  

				d = {  'Email': email,  "temporary_password":temp }
				
				subject, from_email, to = "Password Reset", settings.EMAIL_HOST_USER, "kirajmd@gmail.com"
				text_content = plaintext.render(d)
				html_content = htmly.render(d)
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				r = msg.send()
				logger.info(r)
		except Exception as e:
			logger.info(e)


	return render(request, "resetEmail.html", {'data': data})

