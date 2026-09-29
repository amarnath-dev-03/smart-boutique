from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'title',
            'category',
            'amount',
            'description'
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter expense title'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter amount',
                    'step': '0.01'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 4
                }
            ),
        }