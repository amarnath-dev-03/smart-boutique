from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, default='')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name