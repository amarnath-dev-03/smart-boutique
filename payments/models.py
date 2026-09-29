id="8q7x2p"
from django.db import models

from customers.models import Customer
from orders.models import Order


class Payment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('Cash', 'Cash'),
            ('UPI', 'UPI'),
            ('Card', 'Card'),
            ('Bank Transfer', 'Bank Transfer'),
        ],
        default='Cash'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    notes = models.TextField(
        blank=True,
        default=''
    )

    # Soft Delete / Payment History
    is_deleted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Payment #{self.id} - ₹{self.amount}"


