from django import forms
from osmosis.action_type.models import ActionType

class ActionTypeForm(forms.ModelForm):

	class Meta:
		model = ActionType
		fields = ('name',)
	