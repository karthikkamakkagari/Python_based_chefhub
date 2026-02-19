from django import forms
from .models import CookingItem

class CookingItemForm(forms.ModelForm):
    class Meta:
        model = CookingItem
        fields = [
            'name_en', 'name_te', 'name_ta', 'name_hi', 'name_ka',
            'summary_en', 'summary_te', 'summary_ta', 'summary_hi', 'summary_ka',
            'cost',
            'image',
            'quantity'
        ]

