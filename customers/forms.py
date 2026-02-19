from django import forms
from django.forms import inlineformset_factory
from .models import Customer, CustomerDish, CustomerCookingItem, CustomerIngredient
from dishes.models import Dish
from cooking_items.models import CookingItem
from ingredients.models import Ingredient


# ===============================
# Customer Main Form
# ===============================

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'image', 'reason', 'phone', 'address', 'num_person', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ===============================
# Customer Dish Form
# ===============================

class CustomerDishForm(forms.ModelForm):
    class Meta:
        model = CustomerDish
        fields = ['dish']
        widgets = {
            'dish': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dish'].queryset = Dish.objects.all().order_by('name_en')
        self.fields['dish'].empty_label = "-- Select Dish --"


# ===============================
# Customer Cooking Item Form
# ===============================

class CustomerCookingItemForm(forms.ModelForm):
    class Meta:
        model = CustomerCookingItem
        fields = ['cooking_item']
        widgets = {
            'cooking_item': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cooking_item'].queryset = CookingItem.objects.all().order_by('name_en')
        self.fields['cooking_item'].empty_label = "-- Select Cooking Item --"


# ===============================
# Customer Ingredient Form (FIXED)
# ===============================

class CustomerIngredientForm(forms.ModelForm):
    class Meta:
        model = CustomerIngredient
        fields = ['ingredients', 'quantity']
        widgets = {
            'ingredients': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredients'].queryset = Ingredient.objects.all().order_by('name_en')
        self.fields['ingredients'].empty_label = "-- Select Ingredient Item --"


# ===============================
# Inline Formsets
# ===============================

CustomerDishFormSet = inlineformset_factory(
    Customer,
    CustomerDish,
    form=CustomerDishForm,
    extra=1,
    can_delete=True
)

CustomerCookingItemFormSet = inlineformset_factory(
    Customer,
    CustomerCookingItem,
    form=CustomerCookingItemForm,
    extra=1,
    can_delete=True
)

CustomerIngredientFormSet = inlineformset_factory(
    Customer,
    CustomerIngredient,
    form=CustomerIngredientForm,
    extra=1,
    can_delete=True
)
