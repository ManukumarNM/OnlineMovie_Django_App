from django import forms
from django.contrib.auth.models import User 
from .models import *

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
#         model = Profile
#         fields = ['image']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']