from django.conf import settings
from django.urls import resolve
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


import fnmatch

#from djstripe.utils import subscriber_has_active_subscription
#from djstripe.settings import subscriber_request_callback

from osmosis.app.models import App
from osmosis.program.models import Program


import logging
#logger = logging.getLogger(__name__)
logger = logging.getLogger("django")
dashboard_paths = ("app-detail/", "css-test/")
program_paths =("custom-metrics")

class DashboardMiddleware(MiddlewareMixin):



    def process_request(self, request):

        # First, if in DEBUG mode and with django-debug-toolbar, we skip
        #   this entire process.
        #if request.path == settings.:

        logger.info("path: %s" % request.path)

        if request.path == "/" and request.user.is_authenticated:
            logger.info("redir")
            return redirect('dashboard_main')
        if "app-detail/" in request.path:
            
            paths = request.path.split("app-detail/")     
            app_id = paths[1][:1]
            logger.info(app_id)
            app = App.objects.get(pk=app_id)
            if app.owner.user != request.user:
                return redirect('dashboard_main')

        if "program-detail/" in request.path:
            
            paths = request.path.split("program-detail/")     
            program_id = paths[1][:1]
            logger.info(program_id)
            program = Program.objects.get(pk=program_id)
            if program.app.owner.user != request.user:
                return redirect('dashboard_main')
      
  