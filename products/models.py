from django.db import models

from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField(null=False)

    def __str__(self):
        return f'{self.product.name} {self.customer.email}' 

    class Meta:
        db_table = 'orders'
