from django.contrib import admin
from .models import CookingItem


@admin.register(CookingItem)
class CookingItemAdmin(admin.ModelAdmin):

    list_display = (
        'item_id',
        'name_en',
        'quantity',
        'cost'
    )

    list_filter = (
        'cost',
    )

    search_fields = (
        'item_id',
        'name_en',
        'quantity'
    )

    ordering = ('item_id',)
