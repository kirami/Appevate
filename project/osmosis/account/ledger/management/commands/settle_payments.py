

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
from osmosis.app.models import App
from django.db.models import Sum



import logging, json
logger = logging.getLogger("django")

class Command(BaseCommand):
    help = """Payments
    """

    def handle(self, *args, **options):
        logger.info("Payments")


        #for every ledger item that has a payout, look for auto redeems and execute
        ledger_items = Ledger.objects.filter(payout__isnull = False, payment=None, user__redeem_threshold__gt=0)
        users = ledger_items.values("user").distinct()
        items = []
        total = 0
        ids = []

        for item in users:
            user = User.objects.get(pk=item["user"])
            if user.paypal_email:
                available = Ledger.objects.filter(user=user, payout__isnull=False, payment=None)
                balance = available.aggregate(Sum('amount'))["amount__sum"]

                if user.redeem_threshold <= balance and balance > 0:
                    items.append({"email": user.paypal_email, "amount":balance, "id":user.id, "available": available})
                    total = total + balance
                    ids.append(user.id)

        #logger.info(items)
        
        r = batch_pay(items)
        #logger.info(r)

        if r["success"]:
            pay = Payment.objects.create( amount = total, platform="PayPal", batch_id=r["batch_id"]) 
            logger.info("Successful payments made: batch id %s" % r["batch_id"])
            logger.info("Payment id: %s" % pay.id)
            logger.info("Payments made to: %s" % ids)
                         
            for item in items:
                user = User.objects.get(pk=item["id"])
                #account = Account.objects.get(user = user)
                item["available"].update(payment=pay)

        else:
            logger.info("There was an error")
            logger.info("Message: %s" % r["message"])
                
        



