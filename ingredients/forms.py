from django import forms
from .models import Ingredient

UNIT_CHOICES = [
    ('kg','Kilogram'),
    ('g','Gram'),
    ('pcs','Pieces'),
    ('leaves','Leaves'),
    ('liters','Liters'),
    ('ml','Milliliters'),
    ('spoons','Spoons')
]

class IngredientForm(forms.ModelForm):
    image_url = forms.URLField(
        required=False,
        label='Image URL',
        widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'Enter image URL'})
    )
    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'})
    )

    class Meta:
        model = Ingredient
        fields = ['ingredient_id', 'name_en', 'name_te', 'name_ta', 'name_hi', 'name_ka', 
                  'quantity', 'unit', 'price', 'image', 'image_url']
        widgets = {
            'ingredient_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter ingredient ID'}),
            'name_en': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter English name'}),
            'name_te': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Telugu name'}),
            'name_ta': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Tamil name'}),
            'name_hi': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Hindi name'}),
            'name_ka': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Kannada name'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Quantity'}),
            'price': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price'}),
            'image': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
