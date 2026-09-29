from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'order_date',
        'total_amount',
        'status',
    )

    list_filter = ('status', 'order_date')
    search_fields = (
        'customer__name',
        'customer__phone'
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
        'total',
    )

    list_filter = ('product',)
    search_fields = (
        'order__customer__name',
        'product__name',
    )