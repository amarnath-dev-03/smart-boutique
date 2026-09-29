from django import forms
from .models import Product

class ProductForm(forms.ModelForm):


 class Meta:
    model = Product

    fields = [
        'name',
        'category',
        'price',
        'stock',
        'description'
    ]

    labels = {
        'name': 'Product Name',
        'category': 'Category',
        'price': 'Price',
        'stock': 'Stock Quantity',
        'description': 'Description',
    }

    widgets = {
        'name': forms.TextInput(attrs={
            'placeholder': 'Enter product name'
        }),

        'category': forms.TextInput(attrs={
            'placeholder': 'Enter category'
        }),

        'price': forms.NumberInput(attrs={
            'placeholder': 'Enter price',
            'step': '0.01',
            'min': '0'
        }),

        'stock': forms.NumberInput(attrs={
            'placeholder': 'Enter stock quantity',
            'min': '0'
        }),

        'description': forms.Textarea(attrs={
            'placeholder': 'Enter product description',
            'rows': 4
        }),
    }

