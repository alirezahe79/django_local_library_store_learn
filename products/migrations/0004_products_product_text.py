# Generated by Django 4.0 on 2022-03-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_products_show_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_text',
            field=models.TextField(default='توضیح محصول را وارد نمایید', verbose_name='توضیح محصول'),
        ),
    ]
