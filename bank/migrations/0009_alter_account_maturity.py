# Generated by Django 4.2.5 on 2023-09-29 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0008_alter_account_maturity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='maturity',
            field=models.DateField(null=True),
        ),
    ]
