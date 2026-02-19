from django.db import models
from accounts.models import CustomUser
from dishes.models import Dish
from cooking_items.models import CookingItem
from ingredients.models import Ingredient  
    
class Customer(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='customers/', blank=True, null=True)
    reason = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    num_person = models.IntegerField(default=1)
    email = models.EmailField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    dishes = models.ManyToManyField(Dish, blank=True)
    cooking_items = models.ManyToManyField(CookingItem, blank=True)
    def __str__(self):
        return self.name
    
class CustomerDish(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.name} - {self.dish.name_en}"


class CustomerCookingItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cooking_item = models.ForeignKey(CookingItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    def __str__(self):
        return f"{self.customer.name} - {self.cooking_item.name_en}"

class CustomerIngredient(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.customer.name} - {self.ingredients.name_en}"
    
