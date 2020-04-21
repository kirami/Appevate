from django import forms
from osmosis.program.models import Program

class ProgramFormWizard_1(forms.ModelForm):


	class Meta:
		model = Program
		fields = ('name','app', 'CPA', 'CPC','CPM', 'description' )
		widgets = {'app': forms.HiddenInput()}


class ProgramFormWizard_2(forms.ModelForm):


	class Meta:
		model = Program
		fields = ('budget', )
		widgets = {'app': forms.HiddenInput()}


class ProgramForm(forms.ModelForm):


	class Meta:
		model = Program
		fields = ('name','app', 'CPA', 'CPC','CPM', 'description', 'budget', 'isActive')
		widgets = {'app': forms.HiddenInput()}
