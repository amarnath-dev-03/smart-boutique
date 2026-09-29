from django import forms
from .models import Order, OrderItem
from products.models import Product


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'customer',
            'description',
            'total_amount',
            'status'
        ]


class OrderItemForm(forms.ModelForm):

    product = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by('name'),
        empty_label="Select Product"
    )

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
            'price'
        ]