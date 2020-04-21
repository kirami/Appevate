
from django import forms
from .models import User
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()