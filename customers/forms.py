from django import forms
from .models import Customer, CustomerIngredientList

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerIngredientForm(forms.ModelForm):
    class Meta:
        model = CustomerIngredientList
        fields = '__all__'