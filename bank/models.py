from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


# Data Models
# ===========
class AccountType(models.Model):
    types = [
        (0, "checking"),
        (1, "savings"),
        (2, "money_market"),
        (3, "CD")
    ]

    name = models.CharField(max_length=64, unique=True)
    type = models.IntegerField(choices=types)
    min_deposit = models.DecimalField(decimal_places=2, max_digits=28)
    min_balance = models.DecimalField(decimal_places=2, max_digits=28)
    maintenance_fee = models.DecimalField(decimal_places=2, max_digits=28)
    overdraft_fee = models.DecimalField(decimal_places=2, max_digits=28)
    apy = models.FloatField(default=0)
    maturity_period = models.DurationField(default=timedelta(days=0))

    def __str__(self):
        """Return the string representation of this model."""
        return self.name


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name="accounts")
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=28)
    maturity = models.DateField(null=True, blank=True)

    def __str__(self):
        """Return the string representation of this model."""
        return str(self.id).zfill(10)
    

class Transaction(models.Model):
    description = models.CharField(max_length=256)
    date = models.DateField()
    source = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="withdrawals", null=True, blank=True)
    dest = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="deposits", null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=28)

    def __str__(self):
        """Return the string representation of this model."""
        return str(self.id).zfill(10)
