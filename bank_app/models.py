from django.db import models

from bank_app.choices import *

# Create your models here.

class Account(models.Model):
    account_number = models.IntegerField(null=True, blank=True)
    holder_name = models.CharField(max_length=200, null=True, blank=True)
    holder_email = models.EmailField(max_length=200, null=True, blank=True)
    account_balance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.account_number)+'-'+ str(self.holder_name)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    transaction_detail = models.CharField(max_length=100, null=True, blank=True)
    value_date = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length=50, default='INR', choices=CURRENCY_CHOICES)
    transaction_type = models.CharField(max_length=50, default='DR', choices=TRANSACTION_TYPE_CHOICES)
    transaction_amount = models.FloatField(null=True, blank=True)
    balance_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.account) +'-'+ str(self.id)