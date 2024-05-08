from datetime import date
from decimal import Decimal
import uuid

from django.db.transaction import atomic

from . import models


# Utility Functions
# =================
def transfer_funds(source_account, dest_account, amount):
    """Transfer funds between 2 accounts."""
    # Lookup source and destination accounts
    source = models.Account.objects.get(pk=source_account)
    dest = models.Account.objects.get(pk=dest_account)

    # Prevent negative amount
    if amount <= 0:
        return (False, "Cannot Withdraw Negative or Zero Amount of Funds")

    # Ensure that the source and destination differ
    if source == dest:
        return (False, "Source and Destination Accounts Must Not be the Same")

    # Verify that there are sufficient funds to transfer
    if source.balance < amount:
        # Charge overdraft fee to the source account
        with atomic():
            source.balance -= source.type.overdraft_fee
            source.save()
            transaction = models.Transaction(
                description=f"Overdraft Fee (attempted deposit to account no. {dest})",
                date=date.today(),
                source=source,
                dest=None,
                amount=source.type.overdraft_fee
            )
            transaction.save()
        
        return (False, "Insufficient Funds")
    
    # Verify that the minimum balance will remain in the account
    if source.balance - amount < source.type.min_balance:
        return (False, "Insufficient Minimum Balance")

    # For CD accounts, verify that the maturity has been reached
    if source.type.type == 3 and date.today() < source.maturity:
        return (False, "Account Maturity Not Reached")

    # Perform the funds transfer
    with atomic():
        source.balance -= amount
        source.save()
        dest.balance += amount
        dest.save()
        transaction = models.Transaction(
            description="Electronic Funds Transfer",
            date=date.today(),
            source=source,
            dest=dest,
            amount=amount
        )
        transaction.save()

    return (True, "Success")


def open_account(owner, type, initial_deposit, source_account):
    """Open a new account."""
    # Verify that the initial deposit is sufficient
    account_type = models.AccountType.objects.get(pk=type)

    if initial_deposit < account_type.min_deposit:
        return (False, "Initial Deposit Too Small")

    # Open new account
    with atomic():
        # Create the account
        account = models.Account(
            owner=owner,
            type=account_type
        )

        if account_type.type == 3:
            account.maturity = date.today() + account_type.maturity_period

        elif account_type.type == 1: # temporary promotion
            account.balance = 50

        account.save()

        # Transfer the initial deposit if applicable
        if initial_deposit:
            result = transfer_funds(source_account, account.id, initial_deposit)

            if not result[0]:
                account.delete()

            return result
        
    return (True, "Success")


def pay_monthly_interest(account):
    """Pay monthly interest on an account."""
    interest = account.balance * Decimal((account.type.apy / 12) / 100)

    if not interest:
        return

    with atomic():
        account.balance += interest
        account.save()
        transaction = models.Transaction(
            description="Interest Paid",
            date=date.today(),
            source=None,
            dest=account,
            amount=interest
        )
        transaction.save()


def charge_monthly_maintenance(account):
    """Charge monthly maintentance fee on an account."""
    if not account.type.maintenance_fee:
        return
    
    with atomic():
        account.balance -= account.type.maintenance_fee
        account.save()
        transaction = models.Transaction(
            description="Maintenance Fee",
            date=date.today(),
            source=account,
            dest=None,
            amount=account.type.maintenance_fee
        )
        transaction.save()


# Enable write-ahead log mode if using SQLite
from django.conf import settings

if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    from django.db import connection
    
    with connection.cursor() as cur:
        cur.execute("PRAGMA journal_mode=WAL;")
