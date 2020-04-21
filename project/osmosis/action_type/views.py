from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from osmosis.action_type.models import ActionType

import logging, json
logger = logging.getLogger(__name__)




@login_required
def CreateActionType(request):

	data = {}

	try:
		app = ActionType.objects.create(name=request.POST.get("name"), app_id = request.POST.get("app_id"))
		return HttpResponse(json.dumps({"success":True, "app_id":app.id}), content_type="application/json")
	except Exception as e:
		logger.info(e)
	return HttpResponse(json.dumps({"success":False,  "app_id":app.id}), content_type="application/json")
