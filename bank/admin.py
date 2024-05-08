from django.contrib import admin

from . import models

# Model Admin
# ===========
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]


class AccountAdmin(admin.ModelAdmin):
    list_display = ["get_number", "owner", "type", "get_balance"]
    search_fields = ["id", "owner__username"]

    @admin.display(description="No.")
    def get_number(self, account):
        return str(account)
    
    @admin.display(description="Balance")
    def get_balance(self, account):
        return f"${account.balance:,.2f}"


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["get_number", "description", "date", "source", "dest", "get_amount"]
    search_fields = ["id", "source__id", "dest__id"]

    @admin.display(description="No.")
    def get_number(self, transaction):
        return str(transaction)
    
    @admin.display(description="Amount")
    def get_amount(self, transaction):
        return f"${transaction.amount:,.2f}"


# Register models
admin.site.register(models.AccountType, AccountTypeAdmin)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
