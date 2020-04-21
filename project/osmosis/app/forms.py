from django import forms
from osmosis.app.models import App

class AppForm(forms.ModelForm):

	class Meta:
		model = App
		fields = ('name','url', 'self_payout', 'owner','stripe_id', 'stripe_account', 'image')
	