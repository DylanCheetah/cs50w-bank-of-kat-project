from django import forms

from . import models


# Forms
# =====
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=256)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class OpenAccountForm(forms.Form):
    type = forms.ChoiceField(choices=lambda: [(type.id, f"{type} (min: ${type.min_balance:,.2f})") for type in models.AccountType.objects.all().order_by("name")])
    initial_deposit = forms.DecimalField(min_value=0, decimal_places=2, max_digits=28)
    source_account = forms.CharField(max_length=10, required=False)


class TransferFundsForm(forms.Form):
    destination = forms.CharField(min_length=10, max_length=10)
    amount = forms.DecimalField(min_value=0, decimal_places=2, max_digits=28)
