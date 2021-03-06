from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


# View Products


#...............................................................................................
#.
#.
#.
#..............................// admin products page //.......................................
#.
#.
#.
#...............................................................................................


@user_passes_test(lambda u: u.is_superuser)
def index2(request):
    from .models import Products, Categories

    p = Products.objects.filter(deleted=False)
    list_of_product = []
#     در اینجا ما ار فیلد deleted = False
#     چون میخوایم محصولاتی که پاک نشدن رو بیاره تا به خطا بر نخوریم
    for i in p:
        list_of_product.append([i.name, i.count, i.category.name, i.show_price, i.id])

    cate = list(Categories.objects.all())
    # علت استفاده ار لیست اینکه خروجی all()
    # به صورت آبجکتی ار تمام اون موارد خواسته شده هستش و اینجا میشه تمام دسته بندی مادر
    # به همین دلیل از متد لیست برای تبدیل اون آیجکت به لیست استفاده کردیم
    c = []
    # dict_c= {}
    for i in cate:
        c.append([i.id, i.name])
        # c.append({"id": i.id, "name":i.name})

    return render(request, "product/index.html", {"list": list_of_product, "category": c})


#...............................................................................................
#.
#.
#.
#..............................// User products page //........................................
#.
#.
#.
#...............................................................................................


@login_required(login_url="/account/login")
def index(request):
    from .models import Products, Categories

    c = 10
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

    cate = list(Categories.objects.all())

    # ....................................
    cate1 = Categories.objects.all()
    c_name = []
    for a in cate1:
        c_name.append([a.name])
    # ....................................

    max = list(Products.objects.all())
    max = (len(max) // 10) + 1
    n_page = list(range(1, max + 1, 1))
    befor = 1
    after = 2
    # علت استفاده ار لیست اینکه خروجی all()
    # به صورت آبجکتی ار تمام اون موارد خواسته شده هستش و اینجا میشه تمام دسته بندی مادر
    # به همین دلیل از متد لیست برای تبدیل اون آیجکت به لیست استفاده کردیم
    c = []
    # dict_c= {}
    for i in cate:
        c.append([i.id, i.name])
        # c.append({"id": i.id, "name":i.name})

    return render(request, "product/product.html", {"list": list_of_product, "category": c, "page": n_page,
                                                    "befor": befor, "after": after, "loc_page": 1, "max": max, "c_name": c_name})


#...............................................................................................
#.
#.
#.
#..............................// product details page view //..................................
#.
#.
#.
#...............................................................................................


def product_details(request, subname, id_pro):
    from .models import Products, Subcategorise
    from MYmethod.Tamam import num_sep
    pro_list = []
    try:
        id_pro = int(id_pro)
    except (TypeError, SyntaxError, ValueError):
        # return Http404
        # کامنت بالا برای زمانی هستش که پروژه در هاست آپلود کردیم الان به دلیل خطا نیاز داریم
        return HttpResponse("عدد وارد کنید")
    try:
        subname = str(subname)
    except (TypeError, SyntaxError, ValueError):
        # return Http404
        # کامنت بالا برای زمانی هستش که پروژه در هاست آپلود کردیم الان به دلیل خطا نیاز داریم
        return HttpResponse("مقدار نام زیر دسته بندی را به صورت رشته وارد کنید")

    # در بالا بررسی کردیم که مقدار های ارسال شده برای آیدی حتما عدد
    # و برای نام زیردسته بندی حتما رشته باشد

    try:
        p = Products.objects.get(id=id_pro)
    except Products.DoesNotExist:
        return HttpResponse(" محصول با آیدی " + str(id_pro) + " یافت نشد ")

    # ..............................// comment //..............................
    # در اینجا چون از متد get استفاده کردیم دیگه نیازی به
    # لیست و حلقه for نیست و به همین دلیل ما مستقیما مقدار pرو
    # به عنوان context به قالب ارسال میکنیم
    # pro_list.append([p.name, p.count, p.category.name, p.show_price, p.id, p.product_text])
    # ..............................// comment //..............................

    try:
        sub_cat = Subcategorise.objects.get(name=subname)
    except Subcategorise.DoesNotExist:
        return HttpResponse(" زیردسته بندی با نام " + str(subname) + " یافت نشد ")

    # در اینجا ما براساس دسته بندی محصول محصولات با زیرسته بندی مشابه نمایش میدیم
    sub = Products.objects.filter(category=sub_cat)
    for i in sub:
        if i.id != id_pro:
            pro_list.append([i.name, i.count, i.category.name, i.show_price, i.id])

    for i2 in pro_list:
        print("*")
    return render(request, "product/product_details.html", {"p": p, "list": pro_list})


#...............................................................................................
#.
#.
#.
#.........................// tab Change 2 for single products page //.............................
#.
#.
#.
#...............................................................................................


def TabProducts2(req, page):
    from .models import Products, Subcategorise, Categories
    # در اینجا ما با دریافت نام دسته بندی و زیر دسته بندی از url
    # اونا رو با متد get آیدی شون رو بدست میاریم

    # آیدی دسته بندی و زیر دسته بندی رو بدست آرودیم
    # میتونیم برای بهتر شده کار در صورتی که دسته بندی یا زیردسته بندی وجود نداشت
    # کاربر رو redirect کنیم به صفحه مخصوص 404
    listPro = []
    # در اینجا ما شماره صفحه رو  به عدد تبدیل میکینم
    try:
        num = int(page)
    except (ValueError, TypeError, SyntaxError):
        return redirect("products_home")
        # return HttpResponse("عدد وارد کنید")

    # در اینجا با متغییر n_page تعداد نمایش گزینه هایصفحه رو کنترل میکنیم
    max = list(Products.objects.all())
    max = (len(max) // 10) + 1

    # این شرط چک میکنه اگر عدد صفحه بالا از max بود دیگه به صفحه بعدی نره
    # و دوباره همون صفحه آخر براش لود بشه
    if page > max:
        num = max
        page = max
    n_page = list(range(1, max+1, 1))

    # اگر آیدی وارد شده یک بود از محصول 1 تا 10 رو از حلقه for در
    # لیست ذخیره میکنه
    if num == 1:
        c = 10 * num
        s = 0
        #..............................// comment //..............................
        # این متغییر برای دکمه قبل صفحه هستش
        befor = 1

        # ..............................// comment //..............................
        # این متغییر برای دکمه بعد صفحه هستش
        after = num + 1

        #..............................// comment //..............................
    else:
        # اگر عدد بیشتر از یک بود اونو ضرب در 10 میکنیم
        # بعدش یدونه از اون کم میکنیم و دوباره ضرب در 10 میکنیم
        #  تا اون بازه 10 تایی مورد نظرمون ایجاد کنیم
        c = 10 * num
        s = 10 * (num-1)
        # ..............................// comment //..............................
        # با کم کردن از شماره صفحه صفحه قبل رو بدست میارم
        befor = num - 1

        # ..............................// comment //..............................
        # با اضافه کردن از شماره صفحه صفحه بعد رو بدست میارم
        after = num + 1

        # ..............................// comment //..............................
    # دراین filter زیردسته بندی رو آبجکتش رو در فیلتر قرار دایدم
    pro = Products.objects.all()

    # متغییر n برای ما شمارش تعداد حلقه رو بر عهده میگیره

    # ....................................
    cate1 = Categories.objects.all()
    c_name = []
    for a in cate1:
        c_name.append([a.name])
    # ....................................

    n = 0
    for i in pro:
        n += 1
        if s < n < c:
            # در اینجا چون ما از  and  استفاده کردیم باید هردو شرط درست باشه به همین دلیل
            # ما برابر c در elif قرار دادیم
            listPro.append([i.name, i.count, i.category.name, i.show_price, i.id])
        elif n == c:
            listPro.append([i.name, i.count, i.category.name, i.show_price, i.id])
            break
    return render(req, 'product/product.html', {"list": listPro, "page": n_page, "befor": befor,
                                                "after": after, "loc_page": page, "max": max, "c_name": c_name})


#...............................................................................................
#.
#.
#.
#............................// User products page for categories //..............................
#.
#.
#.
#...............................................................................................


@login_required(login_url="/account/login")
def index_cat(request, namemain):
    from .models import Categories, Products, Subcategorise
    c = 10
    s = 0
    n = 0
    try:
        # ..............................// comment //..............................
        #.
        # در اینجا ما میام با نام دسته بندی یه رسته از اون دسته بندی
        #  از دیتابیس دریافت میکنیم
        #.
        # ..............................// comment //..............................

        c_P = Categories.objects.get(name=namemain)
    except Categories.DoesNotExist:
        return HttpResponse(f" دسته بندی به نام  {namemain} وجود ندارد ")

    # ..............................// comment //..............................
    #.
    # دراینجا تمام زیر دسته های دسته بندی مورد نظر رو میکریم و داخل حلقه for
    # قرار میدیم تا به تک تک زیر دسته ها و محصولاتشون دسترسی داشته باشیم
    #.
    # ..............................// comment //..............................

    s_p = Subcategorise.objects.filter(parent=c_P)
    pro_list = []
    for i in s_p:
        p = Products.objects.filter(deleted=False, category=i)
        for m in p:
            n += 1
            if s < n < c:
                pro_list.append([m.name, m.count, m.category.name, m.show_price, m.id])
            elif n == c:
                pro_list.append([m.name, m.count, m.category.name, m.show_price, m.id])
                break

    # ..............................// important PART //..............................
    #.
    # این حلقه برای دریافت تعداد کامل محصولات دسته بندی هستش و
    #  از اون برای صفحه بندی استفاده میکنیم
    m_c = 0
    sub = Subcategorise.objects.filter(parent=c_P)
    for i in sub:
        p = Products.objects.filter(category=i)
        for m in p:
            m_c += 1
    # ..............................// important PART //..............................
    #.
    # اینجا ما نام تمام دسته بندی ها رو برای نمایش در قالب دریافت میکنیم

    cate1 = Categories.objects.all()
    c_name = []
    for a in cate1:
        c_name.append([a.name])

    # ....................................

    cate = list(Categories.objects.all())
    max = m_c
    max = (max // 10) + 1
    n_page = list(range(1, max + 1, 1))
    befor = 1
    after = 2
    c = []
    subi = 1
    for i in cate:
        c.append([i.id, i.name])
    return render(request, "product/product.html", {"list": pro_list, "category": c, "page": n_page,
                                                    "befor": befor, "after": after, "loc_page": 1, "max": max,
                                                    "c_name": c_name, "subi": subi, "namecat": namemain})


#...........................................................................................
#.
#.
#.
#....................// tab Products for multi subcategorise page  //.......................
#.
#.
#.
#...........................................................................................


def TabProducts(req, namemain, page):
    from .models import Products, Subcategorise

    # ابن تابع برای زمانی که برای زیردستهبندی ها نمایش متفاوتی داشتند استفاده میشه

    # در اینجا ما با دریافت نام دسته بندی و زیر دسته بندی از url
    # اونا رو با متد get آیدی شون رو بدست میاریم
    #
    from .models import Categories
    try:
        # ..............................// comment //..............................
        # .
        # در اینجا ما میام با نام دسته بندی یه رسته از اون دسته بندی
        #  از دیتابیس دریافت میکنیم
        # .
        # ..............................// comment //..............................

        cat = Categories.objects.get(name=namemain)
        x = cat.id
    except Categories.DoesNotExist:
        return redirect("products_home")
        # return HttpResponse("دسته بندی وجود ندارد")

    # آیدی دسته بندی و زیر دسته بندی رو بدست آرودیم
    # میتونیم برای بهتر شده کار در صورتی که دسته بندی یا زیردسته بندی وجود نداشت
    # کاربر رو redirect کنیم به صفحه مخصوص 404
    listPro = []
    # در اینجا ما شماره صفحه رو  به عدد تبدیل میکینم
    try:
        num = int(page)
    except (ValueError, TypeError, SyntaxError):
        return redirect("products_home")
        # return HttpResponse("عدد وارد کنید")

    # این حلقه برای دریافت تعداد کامل محصولات دسته بندی هستش
    m_c = 0
    sub = Subcategorise.objects.filter(parent=cat)
    for i in sub:
        p = Products.objects.filter(category=i)
        for m in p:
            m_c += 1

    # در اینجا با متغییر n_page تعداد نمایش گزینه هایصفحه رو کنترل میکنیم
    max = m_c
    max = (max // 10) + 1

    # این شرط چک میکنه اگر عدد صفحه بالا از max بود دیگه به صفحه بعدی نره
    # و دوباره همون صفحه آخر براش لود بشه
    if page > max:
        num = max
        page = max
    n_page = list(range(1, max + 1, 1))

    # اگر آیدی وارد شده یک بود از محصول 1 تا 10 رو از حلقه for در
    # لیست ذخیره میکنه
    if num == 1:
        c = 10 * num
        s = 0
        befor = 1
        after = num + 1
    else:
        # اگر عدد بیشتر از یک بود اونو ضرب در 10 میکنیم
        # بعدش یدونه از اون کم میکنیم و دوباره ضرب در 10 میکنیم
        #  تا اون بازه 10 تایی مورد نظرمون ایجاد کنیم
        c = 10 * num
        s = 10 * (num - 1)
        befor = num - 1
        after = num + 1
    # دراین filter زیردسته بندی رو آبجکتش رو در فیلتر قرار دایدم

    # ....................................
    cate1 = Categories.objects.all()
    c_name = []
    for a in cate1:
        c_name.append([a.name])
    #....................................

    # ..............................// comment //..............................
    # .
    # دراینجا تمام زیر دسته های دسته بندی مورد نظر رو میکریم و داخل حلقه for
    # قرار میدیم تا به تک تک زیر دسته ها و محصولاتشون دسترسی داشته باشیم
    # .
    # ..............................// comment //..............................
    n = 0
    sub = Subcategorise.objects.filter(parent=cat)
    for p in sub:
        pro = Products.objects.filter(category=p)
        for i in pro:
            n += 1
            if s < n < c:
                # در اینجا چون ما از  and  استفاده کردیم باید هردو شرط درست باشه به همین دلیل
                # ما برابر c در elif قرار دادیم
                listPro.append([i.name, i.count, i.category.name, i.show_price, i.id])
            elif n == c:
                listPro.append([i.name, i.count, i.category.name, i.show_price, i.id])
                break

    # متغییر n برای ما شمارش تعداد حلقه رو بر عهده میگیره

    subi = 1
    return render(req, 'product/product.html', {"list": listPro, "page": n_page, "befor": befor,
                                                "after": after, "loc_page": page, "max": max, "subi": subi,
                                                "namecat": namemain, "c_name": c_name})


#...........................................................................................
#.
#.
#.
#....................// produtcs delete special version  //................................
#.
#.
#.
#...........................................................................................


def delete_pro(request):
    if request.method == "GET":
        command = request.GET.get("command", None)
        id = request.GET.get("id", None)

        try:
            if id:
                id = int(id)
            else:
                raise TypeError
        except TypeError:
            return HttpResponse("داداش اشتباه زدی عدد وارد کن برای id")

        if command == "delete":
            from .models import Products
            try:
                p = Products.objects.get(id=id)
                name = p.name
                # p.delete= True ; p.save()
                p.delete()
                # در اینجا صرفاَ این متد از p برای پاک کردن محصول کافیه و نیازی به save نیست
            except Products.DoesNotExist:
                return HttpResponse("چنین محصولی با آیدی " + str(id) + "وجود ندارد")
        else:
            return HttpResponse("what are you doing bro???" + str(command) + "=command")
        return HttpResponse(name + " : " + str(id) + "پاک شد")
    else:
        return Http404()


#...........................................................................................
#.
#.
#.
#....................// produtcs delete command version  //................................
#.
#.
#.
#...........................................................................................


def delete(request, id_cat=None):
    if not id_cat:
        return redirect("products_home")
    else:
        from .models import Products

        try:
            p = Products.objects.get(id=id_cat)
            p.delete()
            return redirect("products_home")
        except Products.DoesNotExist:
            # در اینجا چون از جمع استفاده کردیم باید همه از یک نوع باشند به همین دلیل
            # این id_cat به رشته تبدیل کردیم
            return HttpResponse("محصول با آیدی  " + str(id_cat) + " وجود ندارد")


#...........................................................................................
#.
#.
#.
#....................// add products with out admin panel  //................................
#.
#.
#.
#...........................................................................................


def add(request):
    if request.method == "POST":
        from .models import Products, Categories, Subcategorise
        from Tamam import num_sep

        name_product = request.POST.get("name_product", False)
        price_product = request.POST.get("price_product", False)
        count_product = request.POST.get("count_product", False)
        subcategory_product = request.POST.get("subcategory_product", False)
        category_product = request.POST.get("category_product", False)
        if False in [name_product, price_product, count_product, subcategory_product, category_product]:
            return HttpResponse("اطلاعات را به طور کامل وارد نمایید")
        else:
            # بررسی اینکه زیر دسته بندی مورد نظر وجود داره یا نه
            try:
                s_c = Subcategorise.objects.get(id=subcategory_product)
            except Subcategorise.DoesNotExist:
                # return HttpResponse("دسته بندی مورد نظر وجود ندارد")
                # یا همچنین میشه از render استفاده کرد و پیغام خطا رو در context اون در همون صفحه نمایش داد
                return redirect("product")
            p = Products()
            p.name = name_product
            # بررسی اینکه کاربر مقدار عددی وارد کرده باشه و مقدار چرت و پرتی وارد نکرده باشه
            try:
                p.price = int(price_product)
                p.count = int(count_product)
            except (ValueError, TypeError, SyntaxError):
                return redirect("product")
            p.show_price = num_sep(p.price)
            p.category = s_c
            p.save()
            return HttpResponse("محصول " + name_product + " با موفقیت اضافه شد")
    else:
        return Http404()


#...........................................................................................
#.
#.
#.
#....................// edit products with out admin panel  //..............................
#.
#.
#.
#...........................................................................................


def edit(request, id_pro=None):
    if not request.user.is_superuser:
        return Http404
    from .models import Products, Subcategorise
    from Tamam import num_sep

    if request.method == "POST":

        name_product = request.POST.get("name_product", False)
        price_product = request.POST.get("price_product", False)
        count_product = request.POST.get("count_product", False)
        category_product = request.POST.get("category_product", False)
        if False in [name_product, price_product, count_product, category_product]:
            return redirect("products_home")
        else:
            try:
                #در اینجا ممکنه که زیردسته بندی وجود
                # نداشته باشه ما اونو از طریق get از  Subcategorise دریافت میکنیم
                try:
                    # در اینجا ما با آچاکس  id ساب Subcategorise رو دریافت میکنیم
                    # و به همین خاطر از id برای دریافت زیردسته بندی استفاده میکنیم
                    s_c = Subcategorise.objects.get(id=category_product)
                    # در اینجا میتونیم با دریافت دسته بندی
                    #علاوه بر زیر دسته بندی امکان ایجاد زیر دسته بندی جدید رو برای
                    # کاربر فراهم کنیم
                except Subcategorise.DoesNotExist:
                    return HttpResponse("دسته یندی مورد نطر وجود ندارد")

                p = Products.objects.get(id=id_pro)

                p.name = name_product
                # بررسی اینکه کاربر مقدار عددی وارد کرده باشه و مقدار چرت و پرتی وارد نکرده باشه
                try:
                    p.price = int(price_product)
                    p.count = int(count_product)
                except (ValueError, TypeError, SyntaxError):
                    return redirect("product")
                p.show_price = num_sep(p.price)
                p.category = s_c
                p.save()
                return redirect("products_home")
            except Products.DoesNotExist:
                return HttpResponse("محصول با آیدی"+str(id_pro)+"وجود ندارد")
    elif request.method == "GET":
        if not id_pro:
            return redirect("products_home")
        else:
            p = Products.objects.filter(id=id_pro, deleted=False)
            if len(p) == 1:
                list_of_product = []
                for i in p:
                    list_of_product.append([i.name, i.count, i.show_price, i.category.name, i.id])

                return render(request, "product/edit.html", {"list": list_of_product})
    raise Http404("محصول یافت نشد")


#...........................................................................................
#.
#.
#.
#....................// get subcategories for ajax  //......................................
#.
#.
#.
#...........................................................................................


def get_subcategories(request):
    from models import Categories, Subcategorise
    if request.method == "POST":
        #در اینجا ما با ajax آیدی دسته بندی رو دریافت می کنیم
        # و چون به صورت رشته هستش باید به int تیدبل بشه
        # علت قرار دادن صفر به عنوان پیشفرض اینکه ما دسته بندی صفر نداریم
        # 0 هم false حساب میشه
        id_cat = int(request.POST.get("category_product", 0))
        dict_sub = []
        if not id_cat:
            return JsonResponse(dict_sub, safe=False)

        # در اینجا ما یک کوئری از دسته بندی رو با آیدی دریافتی می گیریم
        # که اگر دسته بندی مورد نظر وجود نداشته باشه یه لیست خالی به عنوان زیردسته ارسال میشه
        # که در نتیجه در زیر دسته بندی میزنه "هیچ موردی یافت نشد"
        try:
            cat = Categories.objects.get(id=id_cat)
        except Categories.DoesNotExist:
            return JsonResponse(dict_sub, safe=False)

        # در اینجا ما با استفاده ار رکوردی که از دسته بندی گرفتیم
        # رو به عنوان parent زیر دسته بندی در filter قرار میدیم
        # و  در نتیجه به یه لسیت ار تمام زیر دسته هایی که parent اونها دسته بندی مورد نظر ماست رو نشون میده
        s_c = Subcategorise.objects.filter(parent=cat)
        for sub_cats in s_c:
            dict_sub.append({"id": sub_cats.id, "name": sub_cats.name})
            # در اینجا ما لیست خالی dict_sub رو با اعضایی از جنس دیکشنری
            # به کمک حلقه for ایندکس به ایندکس پر میکنیم
            # نام sub_cats یه نام اختیاری برای استفاده در حلقه for هستش
        return JsonResponse(dict_sub, safe=False)
    else:
        return Http404("محصول یا دسته بندی یافت نشد")


def test(request):
    return render(request, "base.html")


#...........................................................................................
#.
#.
#.
#..................// this function import Thousand seprator  //............................
#.
#.
#.
#...........................................................................................


@user_passes_test(lambda u: u.is_superuser)
def number_seprator(request):
    from .models import Products
    import locale
    locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

    # ............................// for host //..............................
    # import locale
    # locale.setlocale(locale.LC_ALL, 'en_US')
    # 'en_US'
    # ............................// for host //..............................

    p = Products.objects.filter(deleted=False)
    for i in p:
        id_pro = i.id
        value = i.price
        value = f'{value:n}'  # For Python ≥3.6

        # ............................// for host //..............................
        # value = locale.format("%d", value, grouping=True)
        # ............................// for host //..............................

        try:
            pro = Products.objects.get(id=id_pro)
            pro.show_price = value
            pro.save()
        except Products.DoesNotExist:
            return HttpResponse(" محصول با آیدی " + str(id_pro) + " یافت نشد ")
    return HttpResponse("همشون حل شد حاجی")

# ..............................// comment //..............................
# این تابع فقط در دسترس super user ها هستش
# و با در خواست دادن به اون تمام show_price ها رو
# به قیمت جدید آپدیت میکنه
# ..............................// comment //..............................