

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


        #for every ledger item that has doesn't have a payout yet
        apps = Ledger.objects.filter(payout=None).values_list("action__action_type__app", flat=True).distinct()
        items = []
        total = 0
        ids = []
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        

        for app in apps:
            app = App.objects.get(pk=app)
            ledger_items =Ledger.objects.filter(payout=None, action__action_type__app=app)
            total = ledger_items.aggregate(Sum('amount'))["amount__sum"]
            total_cents = int( total * 100)
            customer = stripe.Customer.retrieve(app.stripe_id)
            #logger.info(customer)

            r = stripe.Charge.create(amount=str(total_cents),currency="usd",customer=customer,description="Charge for Appevate")

            if r["paid"]:
                #logger.info(r)
                pay = Payout.objects.create(app=app, amount=total)
                ledger_items.update(payout=pay)
                logger.info("App: %s paid out $%s" % (app.id, total))
            else:
                logger.info("App: %s returned an error: $%s" % (app.id, r["failure_code"]))

        #logger.info(items)

        #r = batch_pay(items)
        #logger.info(r)
        """
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
                
        """
        






        #for campaign either billing day or +14 
        
        '''
        now = dt.datetime.now()
        fourteen_ago = now - timedelta(days=14)

        stores = Store.objects.filter(Q(storeaccount__created__day = fourteen_ago.day) | Q(storeaccount__created__day = now.day))
       
        campaigns = Campaign.objects.filter(store__in = stores)
        campaigns = Campaign.objects.filter(pk=34)
        for campaign in campaigns:
            items = campaign.account.ledger_items.filter(
                invoice_item_id = None,
            )
            # Just do a hard check on the total cost first to manage the offer's
            # state
            max_spend = campaign.spending_limit or 0.00
            if max_spend > 0.00 \
                    and max_spend < items.aggregate(total=Sum(F('amount'))):
                campaign.over_budget = True
            else:
                campaign.over_budget = False

            campaign.save()

            # Cycle through them all and increment the settlement amount,
            # grabing all items that are below the amount and adding those to
            # the stripe invoice account so that they can be settled.
            settlable_item_pks = [] 
            total = 0.00

            for item in items:
                if max_spend > 0.00 and max_spend < (item.amount + total):
                    break

                settlable_item_pks.append(item.pk)

            campaign_items = campaign.account.ledger_items.filter(
                pk__in=settlable_item_pks
            )
            amount = campaign_items.aggregate(
                total=Sum(F('amount'))
            )['total']
            customer = Customer.objects.get(subscriber=campaign.advertiser.user)
            
            addedItem = paid = False
            #add any invoice items, if successful charge, then sync if charged
            logger.info("1")
            if amount and amount > config.STRIPE_MINIMUM:
                addedItem = stripe.InvoiceItem.create(
                    customer=customer.stripe_id,
                    invoice=None,
                    amount=int(100 * amount),
                    currency="usd",
                    description="Socialrebate performance"
                ) 
                
                
                if addedItem:
                    #logger.info("added")
                    campaign_items.update(invoice_item_id = addedItem["id"])
                    paid =customer.send_invoice()
                    customer.sync_invoices()
                 
                    if paid:
                        #logger.info("paid")
                        campaign_items.update(state=LedgerItem.SETTLED)
        '''
            