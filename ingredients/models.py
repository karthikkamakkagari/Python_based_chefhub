from django.db import models

UNIT_CHOICES = (
    ('kg','Kilogram'),
    ('g','Gram'),
    ('pcs','Pieces'),
    ('leaves','Leaves'),
    ('liters','Liters'),
    ('ml','Milliliters'),
    ('spoons','Spoons')
)

class Ingredient(models.Model):
    ingredient_id = models.CharField(max_length=10, unique=True)
    name_en = models.CharField("Name (English)", max_length=100, default="Ingredient")
    name_te = models.CharField("Name (Telugu)", max_length=100, blank=True, null=True)
    name_ta = models.CharField("Name (Tamil)", max_length=100, blank=True, null=True)
    name_hi = models.CharField("Name (Hindi)", max_length=100, blank=True, null=True)
    name_ka = models.CharField("Name (Kannada)", max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # new field for URL
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, blank=True, null=True)
    price = models.FloatField(default=0.0)
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
        return self.name_en
