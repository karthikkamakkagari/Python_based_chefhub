from django.db import models
from ingredients.models import Ingredient

UNITS = (
    ('kg', 'Kilogram'),
    ('g', 'Gram'),
    ('pcs', 'Piece'),
    ('leaves', 'Leaves'),
    ('liters', 'Liters'),
    ('ml', 'Milli Liters'),
    ('spoon', 'Spoon'),
    ('N/A', 'N/A'),
)

class Dish(models.Model):
    dish_id = models.CharField(max_length=20, unique=True, blank=True)
    name_en = models.CharField(max_length=100)
    name_te = models.CharField(max_length=100, blank=True, null=True)
    name_ta = models.CharField(max_length=100, blank=True, null=True)
    name_hi = models.CharField(max_length=100, blank=True, null=True)
    name_ka = models.CharField(max_length=100, blank=True, null=True)
    preparation_en = models.TextField(blank=True, null=True)
    preparation_te = models.TextField(blank=True, null=True)
    preparation_ta = models.TextField(blank=True, null=True)
    preparation_hi = models.TextField(blank=True, null=True)
    preparation_ka = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through='DishIngredient')

    def save(self, *args, **kwargs):
        if not self.dish_id:
            last_dish = Dish.objects.order_by("-id").first()
            if last_dish and last_dish.dish_id.startswith("D"):
                last_num = int(last_dish.dish_id[1:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.dish_id = f"D{new_num:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish_id} - {self.name_en}"


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)
    unit = models.CharField(max_length=20, choices=UNITS)
    price = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.ingredient:
            self.price = self.ingredient.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish.name_en} - {self.ingredient.name_en}"
