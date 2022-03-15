from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
# Create your views here.


def home(request):
    if request.user and request.user.is_authenticated:
        from products.models import Products
        # return render(request, "account/dashboard.html")
        c = 8
        s = 0
        p = Products.objects.filter(deleted=False)
        list_of_product = []
        #     در اینجا ما ار فیلد deleted = False
        #     چون میخوایم محصولاتی که پاک نشدن رو بیاره تا به خطا بر نخوریم
        n = 0
        for i in p:
            n += 1
            if s < n < c:
                # در اینجا چون ما از  and  استفاده کردیم باید هردو شرط درست باشه به همین دلیل
                # ما برابر c در elif قرار دادیم
                list_of_product.append([i.name, i.count, i.category.name, i.show_price, i.id])
            elif n == c:
                list_of_product.append([i.name, i.count, i.category.name, i.show_price, i.id])
                break
        return render(request, "dashboard/dashboard.html", {"list": list_of_product})
    return redirect("account_login")