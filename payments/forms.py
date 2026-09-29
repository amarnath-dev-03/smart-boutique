
from django import forms

from .models import Payment
from customers.models import Customer
from orders.models import Order


class PaymentForm(forms.ModelForm):

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by('name'),
        empty_label="Select Customer"
    )

    order = forms.ModelChoiceField(
        queryset=Order.objects.all().order_by('-order_date'),
        empty_label="Select Order"
    )

    class Meta:
        model = Payment

        fields = [
            'customer',
            'order',
            'amount',
            'payment_method',
            'status',
            'notes'
        ]

        widgets = {
            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

