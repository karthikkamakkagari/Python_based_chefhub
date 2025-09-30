from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'token', 'account_type', 'preferred_language','address', 'sex', 'phone_number', 'catering_name', 'profile_picture']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'token', 'account_type', 'preferred_language', 'address',
                  'phone_number', 'sex', 'catering_name', 'profile_picture']