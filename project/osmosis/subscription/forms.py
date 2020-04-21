from django import forms
from djstripe.settings import PLAN_CHOICES


class SubscriptionCreateForm(forms.Form):
    stripeToken = forms.CharField(widget=forms.HiddenInput())
    plan = forms.ChoiceField(choices=PLAN_CHOICES)
