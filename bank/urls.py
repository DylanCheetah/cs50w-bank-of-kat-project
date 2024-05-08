from django.urls import path

from . import views


app_name = "bank"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("account", views.account, name="account"),
    path("account/open", views.open_account, name="open-account"),
    path("account/get", views.get_accounts, name="get-accounts"),
    path("account/<int:id>", views.account_details, name="account-details"),
    path("account/<int:id>/transfer", views.transfer_funds, name="transfer-funds"),
    path("transactions", views.get_transactions, name="get-transactions")
]
