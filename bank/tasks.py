from django.db.utils import OperationalError

from . import models
from . import utils


# Tasks
# =====
def pay_monthly_interest():
    """Pay the monthly interest on each account."""
    for account in models.Account.objects.all():
        while True:
            try:
                utils.pay_monthly_interest(account)
                break

            except OperationalError:
                pass


def charge_monthly_fees():
    """Charge monthly maintenance fees."""
    for account in models.Account.objects.all():
        while True:
            try:
                utils.charge_monthly_maintenance(account)
                break

            except OperationalError:
                pass
