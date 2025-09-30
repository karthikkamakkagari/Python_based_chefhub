from django.contrib import admin
from .models import CookingItem

@admin.register(CookingItem)
class CookingItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name_en', 'unit')
    search_fields = ('item_id', 'name_en', 'name_te', 'name_ta', 'name_hi', 'name_ka')
    list_filter = ('unit',)
