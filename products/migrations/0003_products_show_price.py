# Generated by Django 4.0 on 2022-03-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_categories_id_alter_subcategorise_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='show_price',
            field=models.CharField(blank=True, default='0', max_length=50, verbose_name='قیمت نمایشی'),
        ),
    ]
