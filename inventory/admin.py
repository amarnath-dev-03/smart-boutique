from django.contrib import admin
from .models import InventoryItem


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'quantity',
        'price',
        'created_at',
    )

    list_filter = ('category',)
    search_fields = ('name', 'category')