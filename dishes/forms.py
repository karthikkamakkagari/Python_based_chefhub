from django import forms
from django.forms import inlineformset_factory
from .models import Dish, DishIngredient, UNITS
from ingredients.models import Ingredient



class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            'dish_id',
            'name_en', 'name_te', 'name_ta', 'name_hi', 'name_ka',
            'preparation_en', 'preparation_te', 'preparation_ta',
            'preparation_hi', 'preparation_ka',
            'image'
        ]


class DishIngredientForm(forms.ModelForm):
    class Meta:
        model = DishIngredient
        fields = ['ingredient', 'quantity', 'unit', 'price']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control ingredient-select'}),
            'quantity': forms.NumberInput(attrs={'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'unit-field'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'class': 'price-field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('name_en')
        self.fields['ingredient'].empty_label = "-- Select Ingredient --"

    # def save(self, commit=True):
    #     instance = super().save(commit=False)

    #     # Only auto fill if this is NEW object (no PK)
    #     if not instance.pk and instance.ingredient:
    #         instance.quantity = instance.ingredient.quantity
    #         instance.unit = instance.ingredient.unit
    #         instance.price = instance.ingredient.price

    #     if commit:
    #         instance.save()

    #     return instance
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Only autofill if this is NEW object
        if not instance.pk and instance.ingredient:
            if not instance.price:
                instance.price = instance.ingredient.price
            if not instance.unit:
                instance.unit = instance.ingredient.unit

        if commit:
            instance.save()

        return instance


DishIngredientFormSet = inlineformset_factory(
    Dish,
    DishIngredient,
    form=DishIngredientForm,
    extra=1,
    can_delete=True
)
