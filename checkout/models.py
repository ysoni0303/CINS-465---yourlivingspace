from django.db import models
from accounts.models import Account
from apartment.models import Apartment
class Transaction(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    fees = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
class Application(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Review', 'Review'),
        ('Accepted', 'Accepted')
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True)
    application_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    fees = models.FloatField(default=5)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name