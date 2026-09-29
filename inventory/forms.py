from django import forms
from .models import InventoryItem


class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'name',
            'category',
            'quantity',
            'price',
            'description'
        ]