# Generated by Django 4.0 on 2022-04-13 06:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0002_transactions_amount_alter_transactions_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='payment_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 13, 10, 37, 7, 955869), verbose_name='تاریخ پرداخت'),
        ),
    ]