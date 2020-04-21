from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


from .forms import UserRegistrationForm
from osmosis.owner.forms import OwnerRegistrationForm
from osmosis.app.models import App
from osmosis.utils import encrypt_val, decrypt_val

import logging, uuid
logger = logging.getLogger('django') 
dlogger = logging.getLogger('django') 


def plan_view(request, plan_type):
	data= {}
	template = ""
	if plan_type == "gold":
		template = "gold_plan_list.html"
	elif plan_type == "silver":
		template = "silver_plan_list.html"
	else:
		template = "basic_plan_list.html"
	return render(request, template, {'data': data})

def signup(request):
	if request.method == 'POST':
		logger.info("post")
		form = OwnerRegistrationForm(request.POST)
		logger.info("1")
		if form.is_valid():
			user = form.save()
			#username = form.cleaned_data.get('email')
			#raw_password = form.cleaned_data.get('password1')
			#user = authenticate(username=username, password=raw_password)
			login(request, user)


			#send verify email
			try:
				plaintext = get_template('emails/verify.txt')
				htmly     = get_template('emails/verify.html')
				app_name = form.cleaned_data.get('app_name')
				email = form.cleaned_data.get('email')
				link = settings.SITE_URL + "accounts/verifyEmail/?email="  + email + "&code=" + user.verify_code
				
				d = { 'app': app_name,  'link': link }
				
				subject, from_email, to = "Please verify your email", settings.EMAIL_HOST_USER, email
				text_content = plaintext.render(d)
				html_content = htmly.render(d)
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
				msg.attach_alternative(html_content, "text/html")
				r = msg.send()
			except Exception as e:
				logger.info(e)

			return redirect('integrate')
		else:
			logger.info(form.errors)
			logger.info(form.fields['phone_number'])
			logger.info("not valid")

	else:
		logger.info("else")
		form = OwnerRegistrationForm()
	return render(request, 'signup.html', {'form': form})

@login_required
def integrate(request):
	data = {}
	logger.info(request.user.email)
	app = App.objects.filter(owner__user__email = request.user.email)
	data["key"] = app[0].api_key
	#logger.info(app[0].api_secret)
	data["secret"] = decrypt_val(app[0].api_secret)
	data["app"] = app[0].id

	return render(request, 'integrate.html', {'data': data})


