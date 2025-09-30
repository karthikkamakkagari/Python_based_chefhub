from django.db import models
from accounts.models import CustomUser
from dishes.models import Dish
from cooking_items.models import CookingItem
from ingredients.models import Ingredient  # Only Ingredient needed


class Customer(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='customers/', blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    num_person = models.IntegerField(default=1)
    dishes = models.ManyToManyField(Dish, blank=True, related_name='customers')
    cooking_items = models.ManyToManyField(CookingItem, blank=True, related_name='customers')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

class CustomerIngredient(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    total_quantity = models.FloatField()
    unit = models.CharField(max_length=50, default="g")
    def __str__(self):
        return f"{self.customer} - {self.ingredient}"
    
class CustomerIngredientList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="ingredient_list")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.customer.name} - {self.ingredient.name}"
    
