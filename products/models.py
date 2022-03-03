from django.db import models

# Create your models here.


class Categories(models.Model):
    # id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, verbose_name="نام دسته بندی")


class Subcategorise(models.Model):
    # id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, verbose_name="نام دسته بندی")
    parent = models.ForeignKey(Categories, verbose_name="دسته بندی", on_delete=models.CASCADE)


class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام محصول")
    # در اینجا category اسمش اینه در صورتی که در اصل subcategory  هستش
    category = models.ForeignKey(Subcategorise, verbose_name="نام دسته بندی", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, blank=True, verbose_name="تعداد محصول")
    price = models.PositiveIntegerField(verbose_name="قیمت محصول")
    deleted = models.BooleanField(default=False, blank=True, verbose_name="محصول حذف شده")
