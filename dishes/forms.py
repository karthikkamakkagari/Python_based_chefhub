from django import forms
from .models import Dish, DishIngredient
from ingredients.models import Ingredient
from django.conf import settings

UNITS = (
    ('kg', 'Kilogram'),
    ('g', 'Gram'),
    ('pcs', 'Piece'),
    ('leaves', 'Leaves'),
    ('liters', 'Liters'),
    ('ml', 'Milli Liters'),
    ('spoon', 'Spoon'),
)

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        # do NOT include dish_id (auto-generated)
        fields = [
            'name_en', 'name_te', 'name_ta', 'name_hi', 'name_ka',
            'preparation_en', 'preparation_te', 'preparation_ta', 'preparation_hi', 'preparation_ka',
            'image'
        ]
        widgets = {
            'name_en': forms.TextInput(attrs={'class':'form-control'}),
            'name_te': forms.TextInput(attrs={'class':'form-control'}),
            'name_ta': forms.TextInput(attrs={'class':'form-control'}),
            'name_hi': forms.TextInput(attrs={'class':'form-control'}),
            'name_ka': forms.TextInput(attrs={'class':'form-control'}),
            'preparation_en': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'preparation_te': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'preparation_ta': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'preparation_hi': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'preparation_ka': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class DishIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    unit = forms.ChoiceField(choices=UNITS, widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = DishIngredient
        fields = ['ingredient', 'quantity', 'unit']
