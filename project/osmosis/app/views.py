from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import generic
from osmosis.app.models import App
from osmosis.utils import encrypt_val, decrypt_val
from django.http import HttpResponse

import logging
logger = logging.getLogger("django") 

@login_required
def CSSView(request,app_id):
	try:
		logger.info(app_id)
		app = App.objects.filter(owner=request.user, pk = app_id)[0]
		context = {'app' : app}
		return render(request,"css-test.html", context)
	except Exception as e:
		logger.info(e)
		redirect('/profile')


def reset_test_app(request):
	app = App.objects.get(pk = 1)
	logger.info("in reset, db secret: %s" % app.api_secret)
	if not app.api_secret == encrypt_val('2'):
		app.api_secret = encrypt_val('2')
		logger.info("reseting to %s" % app.api_secret)
		app.save()
	return HttpResponse("The app has been reset.")
	


