from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def WishListView(req):
    pro_dict = {}
    if req.method == "POST":
        id_pro = req.POST.get("id_pro", 0)
        user_id = req.POST.get("user_id", 0)
        try:
            id_pro = int(id_pro)
        except (ValueError, TypeError, SyntaxError):
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
        if not id_pro or id_pro <= 0:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        if user_id:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                print("User.DoesNotExist")
                return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        else:
            print("user_id bug")
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        from products.models import Products
        from .models import WishList

        try:
            p = Products.objects.get(deleted=False, id=id_pro)
        except Products.DoesNotExist:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        try:
            wish = WishList.objects.get(id_user=user, id_product=p)
            return HttpResponse("exist")
        except WishList.DoesNotExist:
            c = WishList()
            cont = 0
            controler = 0
            w_wish = WishList.objects.filter(id_user=user)

            for i in w_wish:
                cont += i.count
                controler = i.controler
            #     در اینجا چک میشه که چه تعداد محصول به لیست علاقه مندی ها اضافه شده
            #  اگر 15 یا کمتر بود یدونه اضافه میکنه
            #  در غیر این صورت اگر از 15 بیشتر بود وارد بدنه else میشه و پیام full برای js میره
            if controler - cont >= 0:
                c.count += 1
                c.unit_price = p.price
                c.total_price += c.unit_price
                c.id_user = user
                c.id_product = p
                c.save()
                return HttpResponse('added')
            else:
                # در اینجا اگر تعداد محصولات لیست علاقه مندی بیشتر از 15 بود پیام full برای js میره
                return HttpResponse('full')
    return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)


@login_required(login_url="/account/login")
def WishListpageView(request):
    from .models import WishList
    from MYmethod.Tamam import num_sep

    user = request.user
    wish = WishList.objects.filter(id_user=user)
    pro_list = []
    for i in wish:
        show_price = num_sep(i.unit_price)
        # برای نمایش بخش وضعیت موجودی محمول ما در اطلاعات ارسالی به قالب موجودی محصول رو هم ارسال میکنیم
        pro_list.append([i.id_product.name, i.id_product.count, show_price, i.id_product.id, i.id_product.category.name])
    return render(request, "wishlist/index.html", {"wish": pro_list})


def delete_wish(request):
    """
            id_product
            id_user
            count
            unit_price
            total_price
        """
    pro_dict = {}
    if request.method == "POST":
        # در اینجا ما آیدی محصول و کاربر رو دریافت میکنیم
        id_pro = request.POST.get("id_pro", 0)
        user_id = request.POST.get("user_id", 0)
        try:
            id_pro = int(id_pro)
        except (ValueError, TypeError, SyntaxError):
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
        if not id_pro or id_pro <= 0:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
        from .models import WishList
        try:
            wish = WishList.objects.get(id_product=id_pro, id_user=user_id)
            if wish.count > 0:
                print("اینجا")
                wish.delete()
                wish = WishList.objects.filter(id_user=user_id)
                if wish.count() > 0:
                    for i in wish:
                        pro_dict.update({i.id_product.id: [i.id_product.name, i.count, i.total_price]})
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
        except WishList.DoesNotExist:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
