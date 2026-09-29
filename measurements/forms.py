from django import forms
from .models import Measurement
from customers.models import Customer


class MeasurementForm(forms.ModelForm):

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        empty_label="Select Customer",
        widget=forms.Select(
            attrs={
                'class': 'customer-select'
            }
        )
    )

    class Meta:
        model = Measurement
        fields = [
            'customer',
            'bust',
            'waist',
            'hip',
            'shoulder',
            'sleeve',
            'length',
            'notes'
        ]
        