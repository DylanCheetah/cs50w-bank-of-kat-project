# Generated by Django 4.2.5 on 2023-10-03 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0011_alter_account_maturity_alter_transaction_dest'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date(2023, 10, 3)),
            preserve_default=False,
        ),
    ]
