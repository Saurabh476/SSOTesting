from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # gives us nested name space for configuration and keeps configuration
    # at one place
    class Meta:
        model = User # this saves to user model
        fields = ['username','email','password1','password2']