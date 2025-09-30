import json
from django.db import models

UNITS = (
    ('kg', 'Kilogram'),
    ('g', 'Gram'),
    ('pcs', 'Piece'),
    ('big', 'Big One'),
    ('small', 'Small One'),
    ('medium', 'Medium One'),
)

class CookingItem(models.Model):
    item_id = models.CharField(max_length=20, unique=True)
    name_en = models.CharField(max_length=100)
    name_te = models.CharField(max_length=100, blank=True, null=True)
    name_ta = models.CharField(max_length=100, blank=True, null=True)
    name_hi = models.CharField(max_length=100, blank=True, null=True)
    name_ka = models.CharField(max_length=100, blank=True, null=True)
    summary_en = models.TextField(blank=True, null=True)
    summary_te = models.TextField(blank=True, null=True)
    summary_ta = models.TextField(blank=True, null=True)
    summary_hi = models.TextField(blank=True, null=True)
    summary_ka = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='cooking_items/', blank=True, null=True)
    unit = models.CharField(max_length=20, choices=UNITS)

    def __str__(self):
        return f"{self.item_id} - {self.name_en}"
