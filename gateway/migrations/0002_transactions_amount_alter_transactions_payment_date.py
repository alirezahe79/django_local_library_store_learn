# Generated by Django 4.0.4 on 2022-04-11 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='amount',
            field=models.IntegerField(blank=True, default=0, verbose_name='مبلغ پرداخت'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='payment_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 11, 19, 43, 35, 455025), verbose_name='تاریخ پرداخت'),
        ),
    ]
