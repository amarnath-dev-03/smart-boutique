from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'order',
        'amount',
        'payment_method',
        'payment_date',
    )

    list_filter = ('payment_method', 'payment_date')
    search_fields = (
        'customer__name',
        'customer__phone',
    )