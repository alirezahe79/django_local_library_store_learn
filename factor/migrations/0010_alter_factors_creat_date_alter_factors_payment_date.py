# Generated by Django 4.0 on 2022-03-04 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factor', '0009_alter_factors_creat_date_alter_factors_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factors',
            name='creat_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 4, 23, 39, 59, 599581), verbose_name='تاریخ ایجاد فاکتور'),
        ),
        migrations.AlterField(
            model_name='factors',
            name='payment_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 4, 23, 39, 59, 599581), verbose_name='تاریخ پرداخت'),
        ),
    ]
