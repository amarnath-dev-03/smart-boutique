
from django.db import models


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Salary', 'Salary'),
        ('Electricity', 'Electricity'),
        ('Materials', 'Materials'),
        ('Maintenance', 'Maintenance'),
        ('Transport', 'Transport'),
        ('Marketing', 'Marketing'),
        ('Other', 'Other'),
    ]

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Other'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expense_date = models.DateField(
        auto_now_add=True
    )

    description = models.TextField(
        blank=True,
        default=''
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

