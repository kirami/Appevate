

from constance import config
from django.core.management.base import BaseCommand
from django.db.models import Sum, F
from datetime import datetime, timedelta
import datetime as dt
from django.db.models import Q

from osmosis.account.ledger.models import Ledger
from osmosis.payment.views import batch_pay
from osmosis.customauth.models import User
from osmosis.payment.models import Payment
from osmosis.payout.models import Payout
from osmosis.action.models import Action
from osmosis.app.models import App
from django.db.models import Sum
from django.conf import settings



import logging, json, stripe
logger = logging.getLogger("django")

class Command(BaseCommand):
    help = """Payouts
    """

    def handle(self, *args, **options):
        logger.info("Payouts for %s" % datetime.now())

        u = User.objects.filter(pk__gt = 1)
        u.delete()
        l = Ledger.objects.all()
        l.delete()
        a = Action.objects.all()
        a.delete()
        
        

