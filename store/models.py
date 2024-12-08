import uuid
from datetime import datetime, timezone

from django.db import models


class Powder(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='powders/')

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    powder = models.ForeignKey(Powder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.powder.price  # рассчитываем общую стоимость покупки
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.name} - {self.powder.name} - {self.quantity} units'
