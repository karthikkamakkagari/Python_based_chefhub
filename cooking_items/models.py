from django.db import models
from django.utils import timezone

UNITS = (
    ('kg', 'Kilogram'),
    ('g', 'Gram'),
    ('pcs', 'Piece'),
    ('big', 'Big One'),
    ('small', 'Small One'),
    ('medium', 'Medium One'),
)

class CookingItem(models.Model):
    item_id = models.PositiveIntegerField(unique=True, blank=True, null=True)

    # Names
    name_en = models.CharField(max_length=100)
    name_te = models.CharField(max_length=100, blank=True, null=True)
    name_ta = models.CharField(max_length=100, blank=True, null=True)
    name_hi = models.CharField(max_length=100, blank=True, null=True)
    name_ka = models.CharField(max_length=100, blank=True, null=True)

    # Summaries
    summary_en = models.TextField(blank=True, null=True)
    summary_te = models.TextField(blank=True, null=True)
    summary_ta = models.TextField(blank=True, null=True)
    summary_hi = models.TextField(blank=True, null=True)
    summary_ka = models.TextField(blank=True, null=True)

    # ✅ NEW COST FIELD
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    image = models.ImageField(upload_to='cooking_items/', blank=True, null=True)
    quantity = models.CharField(max_length=20, choices=UNITS)

    created_at = models.DateTimeField(default=timezone.now)
    def get_name(self, language):
        language_map = {
            "TA": self.name_ta,
            "HI": self.name_hi,
            "TE": self.name_te,
            "KA": self.name_ka,
            "EN": self.name_en,
        }

        return language_map.get(language, self.name_en)

    # ✅ AUTO ITEM ID START FROM 1
    def save(self, *args, **kwargs):
        if not self.item_id:
            last_item = CookingItem.objects.order_by('-item_id').first()
            if last_item and last_item.item_id:
                self.item_id = last_item.item_id + 1
            else:
                self.item_id = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_id} - {self.name_en}"
