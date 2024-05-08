# Bank of Kat

## Description
Bank of Kat is an online banking website. The homepage displays a sample ad for a promotion aimed at getting
people to register and open accounts. Additional ads like the sample one could be arranged in the space below
the sample ad. The top of each page has a navbar with a branding link to the homepage as well as links to
login or register for an account. Once logged in, the links on the navbar change to one for managing your
bank accounts and one for logging out. There is also a friendly welcome banner under the navbar. The account 
management page shows a form for opening a new account followed by a list of your existing accounts. Rather
than loading all the account data at once, account data is loaded 20 items at a time in the background via
Javascript. When you scroll to the bottom of the page, more account data will be loaded in the background.
There is also a progress spinner displayed when data is being loaded in the background. The ID of each
bank account is formatted as a standard 10 digit account number and the balance is properly rounded to 2 
digits. If you click on the account number for an account, you will see its details page. The account
details page displays all the account details such as account number, type, balance, and maturity. It also
displays a form for transferring funds to another account and a list of transactions sorted in descending
order by date. When transferring funds, proper checks are in place to prevent you from doing things such as
transferring money to the account you are withdrawing from, overdrawing from the account (will result in an
overdraft fee), or withdrawing a negative amount of money. You also cannot withdraw so much that the balance
drops below the minimum for the chosen account type. CD accounts cannot be withdrawn until they have
matured. A background task queue pays interest and deducts maintenance fees from all accounts on a scheduled
basis (this is set to 1 minute for testing purposes, it would be set to monthly for production). I have also 
enabled the write-ahead log feature on the SQLite database to help improve performance due to the large 
number of write operations being executed on the database in order to handle the interest and fees.

## Distinctiveness and Complexity
This project meets the distinctiveness and complexity requirements because it is not a search engine 
interface, wiki, e-commerce site, email client, or social media site. It is instead a banking website that
utilizes background task queue provided by the `django-q` package to pay interest and deduct maintenance fees
from a collection of bank accounts as well as providing basic bank account functionality such as opening new
accounts and transferring funds between accounts.

## Instructions
01. install project requirements with pip: ```pip install -r requirements.txt```
02. create superuser (this will be needed for testing purposes): ```python manage.py createsuperuser```
03. start test server: ```python manage.py runserver```
04. start task queue (execute this in a separate terminal): ```python manage.py qcluster```
05. visit the homepage
06. click "Register" and create an account
07. after creating an account, you can logout and log back in to try out the login system
08. click "Account" to view the account management page
09. choose "Standard Savings" from the drop down box, type "0" into the initial deposit box, and leave the
    source account box blank
10. click "Open Account" or press Enter to create a new standard savings account
11. you should get $50 for free like the promotion on the homepage says
12. the background task queue will add interest to the savings account every minute
13. you can log into the admin site to add money to the savings account and then try opening different types
    of accounts by using the account management page to choose an account type, enter the amount of money 
    for the initial deposit, and enter the account number to withdraw the intial deposit from

## Files
```
bank/
    static/
        bank/
            scripts/
                account-details.jsx - implements transaction list for account details page
                account.jsx         - implements account list for account management page
    templates/
        bank/
            account-details.html - implements account details page
            account.html         - implements account management page
            index.html           - implements homepage
            layout.html          - implements overall layout for all pages
            login.html           - implements login page
            register.html        - implements registration page
    admin.py  - implements admin classes for admin site and registers data models
    forms.py  - implements registration, login, open account, and transfer funds forms
    models.py - implements account type, account, and transaction data models
    tasks.py  - implements tasks for monthly interest and fees (used by `django-q`)
    urls.py   - defines the URL mappings for the online banking app
    utils.py  - implements utility functions for account management
    views.py  - implements homepage, registration, login, logout, account management, and REST API views
capstone/
    settings.py - defines website settings
    urls.py     - defines the URL mappings for the website
requirements.txt - a list of the dependencies for the website
```
