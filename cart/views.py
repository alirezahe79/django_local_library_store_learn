from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


#...............................................................................................
#.
#.
#.
#..............................// cart index view //............................................
#.
#.
#.
#...............................................................................................


@login_required(login_url="/account/login")
def index(request):
    from .models import Cart
    from MYmethod.Tamam import num_sep

    user = request.user
    # اینجا میریم برای گرفتن سبد تمام محصولات کاربر با آیدی موردنظر
    cart = Cart.objects.filter(id_user=user)
    # در اینجا نام رشته آیدی کاربر با نامی که در جدول های دیتابیس قرار دادیم برابره
    # id_user= user
    pro_list = []
    total_price = 0
    for i in cart:
        # علت انجام این کار اینکه که اگر قیمت تغییر کرده باشه و نمایش اونو
        # یادمون رفته باشه تغییر بدیم برای کاربر قیمت درست رو نمایش میده
        show_price = num_sep(i.id_product.price)
        show_total = num_sep(i.total_price)

        # ..............................// comment //..............................
        # در اینجا ما برای نمایش اعداد به طور دلخواه موارد قبلی را برداشته
        # و جایگزین موارد جدید کردیم
        # و این تغییر صرفا ظاهری بوده و در ساختار سبد خرید هیچ تغییری ندادیم
        # در اینجا ما از رشته سبد ، آبجکت محصول رو درآوردیم تا به نام و قیمت محصول بررسیم

        #  در اینجا ما برای اینکه که به نام زیردسته بندی برسیم i.id_product.category.name استفاده کردیم
        # ..............................// comment //..............................

        pro_list.append([i.id_product.name, i.count, show_price, show_total, i.id_product.id, i.id_product.category.name])
        # pro_list.append([i.id_product.name, i.count, i.unit_price, i.total_price, i.id_product.id])
        total_price += i.total_price

    # ..............................// comment //..............................

    # در پایان بدنه for قیمت نهایی رو به عدد با جدا کننده تبدیل میکنم

    # ..............................// comment //..............................
    gheymat = total_price
    total_price = num_sep(total_price)
    return render(request, "cart/index.html", {"pro": pro_list, "total_price": total_price, "show_sabad": gheymat})


#...............................................................................................
#.
#.
#.
#..............................// add to cart with out ajax//...................................
#.
#.
#.
#...............................................................................................


@login_required(login_url="/account/login")
def add_cart(request, id_pro=None):
    from products.models import Products

    try:
        id_pro = int(id_pro)
    except (ValueError, TypeError, SyntaxError):
        return redirect("products_home")
    if not id_pro or id_pro <= 0:
        return redirect("products_home")

    try:
        p = Products.objects.get(deleted=False, id=id_pro)

    except Products.DoesNotExist:
        return redirect("products_home")
    from .models import Cart
    user = request.user
    pro_list = []
    total_price = 0
    # این برای اینکه برای کابر مورد نظر یه سبد ایجاد کنیم یا به سبد قبلی یدونه اضافه کنیم

    try:
        c = Cart.objects.get(id_user=user, id_product=p)

        # این if به معنی اینکه که ببین محصول موجودی داره یا نه
        c_cuont = c.count + 1
        if p.count - c_cuont >= 0:
            c.count += 1
            # p.count -= 1
            # یدونه از موجودی محصول کم میکنیم
            # p.save()
            c.unit_price = p.price
            c.total_price += c.unit_price
            # برای جمع کردن قیمت مجموع محصول که اگر اولین محصول باشه
            # چون با صفر جمع میشه و اگر اولین نباشه یدونه یدونه به ازای هر request یک بار جمع میشه
            c.save()

        else:
            return HttpResponse("سقف موجودی محصول")
    except Cart.DoesNotExist:
        # در اینجا چون سبدی با آیذی محصول و کاربر وجود نداشت یدونه جدید میسازیم
        c = Cart()
        c.id_user = user
        if p.count > 0:
            c.id_product = p
            c.count += 1
            c.unit_price = p.price
            c.total_price += c.unit_price
            # برای جمع کردن قیمت مجموع محصول که اگر اولین محصول باشه
            # چون با صفر جمع میشه و اگر اولین نباشه یدونه یدونه به ازای هر request یک بار جمع میشه
            c.save()
        else:
            return HttpResponse("خطای 2")

    # اینجا میریم برای گرفتن سبد تمام محصولات کاربر با آیدی موردنظر
    cart = Cart.objects.filter(id_user=user)
    # در اینجا نام رشته آیدی کاربر با نامی که در جدول های دیتابیس قرار دادیم برابره
    # id_user= user
    pro_list = []
    total_price = 0
    for i in cart:
        # در اینجا ما از رشته سبد ، آبجکت محصول رو درآوردیم تا به نام و قیمت محصول بررسیم
        pro = i.id_product
        pro_name = Products.objects.get(id=pro)
        name = pro_name.name
        id_proo = pro_name.id
        pro_list.append([name, i.count, i.unit_price, i.total_price, id_proo])
        total_price += i.total_price
    return render(request, "cart/index.html", {"pro": pro_list, "total_price": total_price})


#...............................................................................................
#.
#.
#.
#..............................// add to cart with ajax and api//...............................
#.
#.
#.
#...............................................................................................


def add_api_cart(req):
    """ api for add product in cart of user """
    """
        models field :
            id_product 
            id_user
            count
            total_price
    """
    pro_dict = {}
    if req.method == "POST":
        id_pro = req.POST.get("id_pro", 0)
        # user_id = req.user.id
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
                return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        else:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        from products.models import Products
        from .models import Cart

        try:
            p = Products.objects.get(deleted=False, id=id_pro)
        except Products.DoesNotExist:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

        try:

            cart = Cart.objects.get(id_user=user, id_product=p)
            # در اینجا چک میکنه که توی انبار محصول موجود باشه تا به سبد اضافه کنه

            c_cuont = cart.count + 1
            if p.count-c_cuont >= 0:
                # cart.store_pro -= 1
                cart.count += 1
                # p.count -= 1
                # p.save()
                cart.unit_price = p.price
                cart.total_price += cart.unit_price
                cart.save()
                # return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
            else:
                return HttpResponse("out of num")

        except Cart.DoesNotExist:
            c = Cart()
            if p.count > 0:
                c.count += 1
                # در اینجا چون محصول در سبد وجود نداشته یدونه سبد جدید ساخته شده
                # و ما برای اولین بار به انبار محصول مقدار میدیم
                # و یدونه به خاطر اضفه شدن به سبد جدید از موجودی انبار کم میکنیم
                c.unit_price = p.price
                c.total_price += c.unit_price
            c.id_user = user
            c.id_product = p
            c.save()

        cart = Cart.objects.filter(id_user=user)
        if cart.count() > 0:
            for c in cart:
                pro_dict.update({c.id_product.id: [c.id_product.name, c.count, c.total_price]})

    return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)


#...............................................................................................
#.
#.
#.
#...........................// delete cart num with ajax and api //.............................
#.
#.
#.
#...............................................................................................


def delete_cart_num(request):
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
        from .models import Cart
        try:
            cart = Cart.objects.get(id_product=id_pro, id_user=user_id)
            if cart.count > 0:
                cart.count -= 1
                # در اینجا قیمت واحد محصول رو از قیمت کل کم میکنیم
                cart.total_price -= cart.unit_price
                cart.save()
                cart = Cart.objects.filter(id_user=user_id)
                if cart.count() > 0:
                    for c in cart:
                        pro_dict.update({c.id_product.id: [c.id_product.name, c.count, c.total_price]})

            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
        except Cart.DoesNotExist:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)


#...............................................................................................
#.
#.
#.
#........................// delete cart row with ajax and api //................................
#.
#.
#.
#...............................................................................................


def delete_cart(request):
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
        from .models import Cart
        try:
            cart = Cart.objects.get(id_product=id_pro, id_user=user_id)
            if cart.count > 0:
                cart.delete()
                cart = Cart.objects.filter(id_user=user_id)
                if cart.count() > 0:
                    for c in cart:
                        pro_dict.update({c.id_product.id: [c.id_product.name, c.count, c.total_price]})

            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)
        except Cart.DoesNotExist:
            return JsonResponse(pro_dict, json_dumps_params={'ensure_ascii': False}, safe=True)

