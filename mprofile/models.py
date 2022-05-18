from django.db import models
from django.contrib.auth.models import User

# Create your models here.

states = (
        ('1', 'تهران'),
        ('2', 'خوزستان'),
        ('3', 'بوشهر'),
        ('4', 'خراسان رضوی'),
        ('5', 'اصفهان'),
        ('6', 'فارس'),
        ('7', 'آذربایجان شرقی'),
        ('8', 'مازندران'),
        ('9', 'کرمان'),
        ('10', 'البرز'),
        ('11', 'گیلان'),
        ('12', 'کهگیلویه و بویراحمد'),
        ('13', 'آذربایجان غربی'),
        ('14', 'هرمزگان'),
        ('15', 'مرکزی'),
        ('16', 'یزد'),
        ('17', 'کرمانشاه'),
        ('14', 'هرمزگان'),
        ('14', 'هرمزگان'),
        ('14', 'هرمزگان'),
        ('14', 'هرمزگان'),
        ('14', 'هرمزگان'),
    )


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name="نام کاربر", on_delete=models.CASCADE)
    state = models.CharField(choices=states, verbose_name="استان", blank=True, max_length=2)
    city = models.CharField(verbose_name="شهر", blank=True, max_length=50)
    zipcod = models.IntegerField(verbose_name="کد پستی", blank=True)
    phone_number = models.IntegerField(verbose_name="شماره تماس", blank=True, default=98)
    address = models.TextField(verbose_name="آدرس", blank=True, max_length=288)