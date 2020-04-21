from django import forms
from osmosis.metric.models import Metric

class MetricForm(forms.ModelForm):

	class Meta:
		model = Metric
		fields = ('name','program','first', 'second')
		widgets = {'program': forms.HiddenInput()}
