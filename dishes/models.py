from django.db import models
from ingredients.models import Ingredient

UNITS = [
    ('kg','Kilogram'),
    ('g','Gram'),
    ('pcs','Pieces'),
    ('leaves','Leaves'),
    ('liters','Liters'),
    ('ml','Milliliters'),
    ('spoons','Spoons')
]


class Dish(models.Model):
    dish_id = models.CharField(max_length=10, unique=True)

    name_en = models.CharField(max_length=255)
    name_te = models.CharField(max_length=255, blank=True, null=True)
    name_ta = models.CharField(max_length=255, blank=True, null=True)
    name_hi = models.CharField(max_length=255, blank=True, null=True)
    name_ka = models.CharField(max_length=255, blank=True, null=True)

    preparation_en = models.TextField(blank=True, null=True)
    preparation_te = models.TextField(blank=True, null=True)
    preparation_ta = models.TextField(blank=True, null=True)
    preparation_hi = models.TextField(blank=True, null=True)
    preparation_ka = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="dish_images/", blank=True, null=True)
    def get_name(self, language):
        language_map = {
            "TA": self.name_ta,
            "HI": self.name_hi,
            "TE": self.name_te,
            "KA": self.name_ka,
            "EN": self.name_en,
        }

        return language_map.get(language, self.name_en)

    def __str__(self):
        return f"{self.dish_id} - {self.name_en}"

    
    
class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, choices=UNITS, default="N/A")
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.dish.name_en} - {self.ingredient.name_en}"



