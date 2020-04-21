from random import random
from datetime import datetime
from hashlib import sha1 as sha_constructor

from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from osmosis.owner.models import Owner
from osmosis.app.models import App

import logging, uuid
logger = logging.getLogger(__name__) 

User = get_user_model()


class OwnerRegistrationForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    app_name = forms.CharField(
        label=_("App Name"),

    )
    app_url = forms.CharField(
        label=_("App URL"),
    )

    first_name = forms.CharField(
        label=_("First Name"),
    )

    last_name = forms.CharField(
        label=_("Last Name"),
    )

    password1 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
       # help_text=_("Enter password")
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        #help_text=_("Enter the same password as before, for verification.")
    )
    
    tos_agree = forms.BooleanField(required=True, label="You must agree to our Terms of Service")

    class Meta:
        model = User
        fields = ("email", "phone_number")

    def __init__(self, *args, **kwargs):
        super(OwnerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['phone_number'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )
        return email
    """
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        return password2
    """

    def save(self, commit=True):
        user = super(OwnerRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            salt = sha_constructor(str(random())).hexdigest()[:5]
            confirmation_key = sha_constructor(salt + user.email).hexdigest()

            #make owner
            logger.info(user)
            owner = Owner.objects.create(user=user, email = user.email, first_name=self.cleaned_data["first_name"], last_name = self.cleaned_data["last_name"])
            key = uuid.uuid4().hex
            secrect = uuid.uuid4().hex
            app = App.objects.create(owner = owner, name = self.cleaned_data["app_name"], 
                url = self.cleaned_data["app_url"], api_key=key, api_secret = secrect )


            
        return user
    