from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, Profile

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['school_id',  'full_name', 'username', 'password1', 'password2', 'email', 'bio', 'gender']


        