import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import forms
from . import models
from . import utils


# Views
# =====
def index(request):
    return render(request, "bank/index.html")


def register(request):
    # Redirect to homepage if logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("bank:index"))

    # Handle submitted form data
    if request.method == "POST":
        # Validate form data
        form = forms.RegisterForm(request.POST)

        if not form.is_valid():
            # Redisplay the form with an error message
            return render(request, "bank/register.html", {
                "form": form,
                "error": "Invalid Form Data"
            })
        
        if form.cleaned_data["password"] != form.cleaned_data["confirm_password"]:
            # Redisplay the form with an error message
            return render(request, "bank/register.html", {
                "form": form,
                "error": "The given passwords did not match."
            })
        
        # Create new user account
        user = User.objects.create_user(
            form.cleaned_data["username"], 
            form.cleaned_data["email"], 
            form.cleaned_data["password"]
        )

        # Login
        login(request, user)

        # Redirect to homepage
        return HttpResponseRedirect(reverse("bank:index"))

    # Display account registration form
    return render(request, "bank/register.html", {
        "form": forms.RegisterForm()
    })


def login_view(request):
    # Redirect to homepage if logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("bank:index"))
    
    # Handle submitted form data
    if request.method == "POST":
        # Validate form data
        form = forms.LoginForm(request.POST)

        if not form.is_valid():
            # Redisplay login form
            return render(request, "bank/login.html", {
                "form": form,
                "error": "Invalid Form Data"
            })
        
        # Attempt to authenticate
        user = authenticate(
            request, 
            username=form.cleaned_data["username"], 
            password=form.cleaned_data["password"]
        )

        if user is None:
            # Redisplay login form
            return render(request, "bank/login.html", {
                "form": form,
                "error": "Invalid Credentials"
            })
        
        # Login and redirect
        login(request, user)

        if "next" in request.GET:
            return HttpResponseRedirect(request.GET["next"])
        
        return HttpResponseRedirect(reverse("bank:index"))
    
    # Display login form
    return render(request, "bank/login.html", {
        "form": forms.LoginForm()
    })


def logout_view(request):
    # Logout and redirect to homepage
    logout(request)
    return HttpResponseRedirect(reverse("bank:index"))


@login_required(login_url="/login")
def account(request):
    return render(request, "bank/account.html", {
        "form": forms.OpenAccountForm()
    })


@login_required(login_url="/login")
def open_account(request):
    # Handle submitted form data
    if request.method == "POST":
        # Validate form data
        form = forms.OpenAccountForm(request.POST)

        if not form.is_valid():
            # Redisplay open account form
            return render(request, "bank/account.html", {
                "form": form,
                "error": "Invalid Form Data"
            })
        
        type = models.AccountType.objects.get(pk=form.cleaned_data["type"])

        if form.cleaned_data["initial_deposit"] < type.min_deposit:
            # Redisplay open account form
            return render(request, "bank/account.html", {
                "form": form,
                "error": "Initial balance less than the minimum deposit amount."
            })
        
        if form.cleaned_data["initial_deposit"] > 0 and form.cleaned_data["source_account"] == "":
            # Redisplay open account form
            return render(request, "bank/account.html", {
                "form": form,
                "error": "No source account given for initial deposit."
            })
        
        # Open the new account
        success, msg = utils.open_account(
            request.user, 
            form.cleaned_data["type"],
            form.cleaned_data["initial_deposit"],
            form.cleaned_data["source_account"]
        )

        if not success:
            # Redisplay open account form
            return render(request, "bank/account.html", {
                "form": form,
                "error": msg
            })
        
        # Redirect to account page
        return HttpResponseRedirect(reverse("bank:account"))
        
    # Ignore GET requests
    return HttpResponseRedirect(reverse("bank:index"))


@login_required(login_url="/login")
def get_accounts(request):
    # Get account data
    start = int(request.GET["start"])
    end = start + int(request.GET["count"])
    accounts = [
        {
            "id": account.id, 
            "number": str(account), 
            "type": account.type.name, 
            "balance": account.balance, 
            "maturity": account.maturity if account.maturity is not None else "n/a"
        } for account in request.user.accounts.all()[start:end]
    ]
    return JsonResponse({"accounts": accounts})


@login_required(login_url="/login")
def account_details(request, id):
    account = models.Account.objects.get(pk=id)

    # Prevent viewing other people's accounts
    if request.user != account.owner:
        raise Http404()

    return render(request, "bank/account-details.html", {
        "account": account,
        "form": forms.TransferFundsForm()
    })


@login_required(login_url="/login")
def transfer_funds(request, id):
    # Prevent transferring funds out of other people's accounts
    source = models.Account.objects.get(pk=id)

    if request.user != source.owner:
        raise Http404()

    # Handle submitted form data
    if request.method == "POST":
        # Validate form data
        form = forms.TransferFundsForm(request.POST)

        if not form.is_valid():
            # Redisplay form
            return render(request, "bank/account-details.html", {
                "account": models.Account.objects.get(pk=id),
                "form": form,
                "error": "Invalid Form Data"
            })
        
        # Do funds transfer
        success, msg = utils.transfer_funds(id, form.cleaned_data["destination"], form.cleaned_data["amount"])

        if not success:
            # Redisplay form
            return render(request, "bank/account-details.html", {
                "account": models.Account.objects.get(pk=id),
                "form": form,
                "error": msg
            })

        # Redirect to account page
        return HttpResponseRedirect(reverse("bank:account-details", args=(id,)))

    # Ignore GET requests
    return HttpResponseRedirect(reverse("bank:index"))


@login_required(login_url="/login")
def get_transactions(request):
    account = models.Account.objects.get(pk=int(request.GET["account_id"]))

    # Prevent viewing other people's transactions
    if request.user != account.owner:
        raise Http404()
    
    start = int(request.GET["start"])
    end = start + int(request.GET["count"])
    transactions = [
        {
            "date": transaction.date, 
            "description": transaction.description, 
            "source": str(transaction.source), 
            "dest": str(transaction.dest), 
            "amount": transaction.amount
        } for transaction in (account.withdrawals.all() | account.deposits.all()).order_by("date", "id").reverse()[start:end]
    ]
    return JsonResponse({"transactions": transactions})
