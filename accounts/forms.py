from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'token', 'account_type', 'preferred_language','address', 'sex', 'phone_number', 'catering_name', 'profile_picture']

class UpdateUserForm(forms.ModelForm):
    token = forms.IntegerField(min_value=0, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'token', 'account_type', 'preferred_language', 'address',
                  'phone_number', 'sex', 'catering_name', 'profile_picture']
    
    def clean_token(self):
        token = self.cleaned_data.get('token')
        if self.instance.account_type == 'SUPREM':
            return 999999
        return token
