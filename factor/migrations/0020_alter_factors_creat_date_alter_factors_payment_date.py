# Generated by Django 4.0 on 2022-05-02 12:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factor', '0019_alter_factors_creat_date_alter_factors_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factors',
            name='creat_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 2, 17, 0, 39, 295428), verbose_name='تاریخ ایجاد فاکتور'),
        ),
        migrations.AlterField(
            model_name='factors',
            name='payment_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 2, 17, 0, 39, 294428), verbose_name='تاریخ پرداخت'),
        ),
    ]
