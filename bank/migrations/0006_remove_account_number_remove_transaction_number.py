# Generated by Django 4.2.5 on 2023-09-28 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_alter_transaction_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='number',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='number',
        ),
    ]