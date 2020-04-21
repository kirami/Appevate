from datetime import datetime
import stripe

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.conf import settings

from braces.views import FormValidMessageMixin
from djstripe.models import Customer, CurrentSubscription
from djstripe.settings import (
    subscriber_request_callback, PLAN_CHOICES, PAYMENT_PLANS, PLAN_LIST
)

#from osmosis.subscription.decorators import advertiser_required_message
from osmosis.subscription.forms import SubscriptionCreateForm



class SubscriptionCreateView(FormValidMessageMixin, FormView):
    template_name = 'create.html'
    form_class = SubscriptionCreateForm
    success_url = '/'
    form_valid_message = 'Welcome to socialrebate! Your subscription is active.'

    #@method_decorator(advertiser_required_message)
    def dispatch(self, request, *args, **kwargs):
        return super(
            SubscriptionCreateView, self
        ).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(
            SubscriptionCreateView, self
        ).get_context_data(*args, **kwargs)
        context.update({
            'PLAN_CHOICES': PLAN_CHOICES,
            'plans': PLAN_LIST,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })

        return context

    def get(self, request, *args, **kwargs):
        customer, created = Customer.get_or_create(
            subscriber=subscriber_request_callback(self.request)
        )

        if hasattr(customer, "current_subscription") and \
                customer.current_subscription.status != CurrentSubscription.STATUS_CANCELLED:
            message = "You are already subscribed."
            messages.info(request, message, fail_silently=True)
            return redirect("djstripe:account")

        return super(SubscriptionCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                customer, created = Customer.get_or_create(
                    subscriber=subscriber_request_callback(self.request))
                customer.update_card(self.request.POST.get("stripeToken"))
                customer.subscribe(form.cleaned_data["plan"])
            except stripe.StripeError as exc:
                form.add_error(None, str(exc))
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
