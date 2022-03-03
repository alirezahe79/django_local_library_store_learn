from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.


class Cart(models.Model):
    id_product = models.ForeignKey(Products, verbose_name="نام محصول", on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, verbose_name="نام کاربر", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, blank=True, verbose_name="تعداد محصول")
    unit_price = models.PositiveIntegerField(default=0, blank=True, verbose_name="قیمت واحد")
    total_price = models.PositiveIntegerField(default=0, blank=True, verbose_name="مبلغ نهایی")
