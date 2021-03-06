# Generated by Django 4.0 on 2022-04-29 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(blank=True, max_length=50, verbose_name='استان')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='شهر')),
                ('zipcod', models.IntegerField(blank=True, verbose_name='کد پستی')),
                ('address', models.TextField(blank=True, max_length=288, verbose_name='آدرس')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='نام کاربر')),
            ],
        ),
    ]
