from django.db import models
from django.contrib.auth.models import User
from products.models import Products
from datetime import datetime
# Create your models here.

factor_state = (
    (0, "پرداخت نشده"),
    (2, "در انتظار پرداخت"),
    (1, "پرداخت شده"),
)
#...................................//  important point //......................................
#.
# کلاس factors به ما اطلاعات کاربر ، قیمت نمایی ، تاریخ پرداخت ، شناسه پرداخت ، و وضعیت پرداخت رو
# به ما میده
# که میشه همون اطلاعات هدر فاکتور و مبلغ نهایی فاکتور
#.
#...................................//  important point //......................................


class Factors(models.Model):
    id_user = models.ForeignKey(User, verbose_name="نام کاربر", on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=datetime.now(), blank=True, verbose_name="تاریخ پرداخت")
    state = models.SmallIntegerField(choices=factor_state, default=1, blank=True, verbose_name="وضعیت پرداخت")
    ref_id = models.CharField(max_length=20, default="", blank=True, verbose_name="کد پیگیری")
    creat_date = models.DateTimeField(default=datetime.now(), blank=True, verbose_name="تاریخ ایجاد فاکتور")
    total_price = models.PositiveIntegerField(verbose_name="مبلغ نهایی", blank=True, default=0)


#...................................//  important point //......................................
#.
# کلاس FactoreProducts به ریز اطلاعات تک تک محصولات خریداری شده توسط کاربر رو میده
# ما برای دریافت اطلاعات فاکتور مورد نظر باید یک فیلد شماره تراکنش
# به کلاس factors  اضافه کنیم که با وارد کردن اون به اطلاعات فاکتور مورد نظر به راحتی
# دسترسی پیدا کنیم حتی در حالتی که کاربر در یک روز چند تراکنش داشته باشد
# که ما برای این منظور از کد پیگیری تراکنش درگاه بانکی استفاده میکنیم
# و همچنین در کنار شماره تراکنش از آبجکت User هم در کنارش برای
# به دست آرودن اطلاعات فاکتور مورد نظر استفاده می کنیم
#.
#...................................//  important point //......................................


class FacotrProduct(models.Model):
    id_factor = models.ForeignKey(Factors, verbose_name="فاکتور", on_delete=models.CASCADE)
    id_product = models.ForeignKey(Products, verbose_name="نام محصول", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1, blank=True, verbose_name="تعداد محصول")
    unit_price = models.PositiveIntegerField(default=0, blank=True, verbose_name="قیمت واحد")
    total_price = models.PositiveIntegerField(verbose_name="مبلغ نهایی")