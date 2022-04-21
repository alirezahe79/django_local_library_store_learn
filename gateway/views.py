from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
import requests
import json
from .models import Transactions

MERCHANT = '20464bc2-ff0e-4ee1-b4ec-63c870723169'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/gateway/verify/'


def send_request(request):
    resp = {"error": "amount not set", "state": False, "authority": ""}

    # ........................//  comment //..............................
    # .
    # در ابن بخش پایین ما از درخواستی که با آجاکس از سبد خرید به این ویو ارسال کردیم
    # مقدار مبلغ نهایی رو دریافت میکنیم
    # .
    # ........................//  comment //..............................

    amount = request.POST.get("amount", None)
    print(amount)
    if not amount:
        return JsonResponse(resp)
    try:
        amount = int(amount)
        # در ابنجا چون برای درگاه پرداخت قیمت باید به ریال باشه ما قیمت کل رو در 10 ضرب میکنیم
        #  تا قیمت به ریال تبدیل بشه تا اونو به درگاه درسال کنیم
        amount_r = amount * 10
    except (ValueError, TypeError):
        return JsonResponse(resp)
    # در اینجا ما تمام اطلاعات لازم رو به درگاه اراسال میکنیم تا درگاه برای ما
    # یه شناسه برای مبلغ مورد نظر م ایجاد کنه تا ما با اون
    # کاربر رو به درگاه مورد نطر منتقل کنبم
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount_r,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    # در اینحا ما بعد از تعیین کردن هدر درخواست
    # اطلاعات رو با متد POST  به کمک با requests برای درگاه ارسال می کنیم
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    # در اینجا بعد از ارسال اطلاعات به زرین پال برای ما به صورت Json اطلاعاتی ارسال میشه
    # که بخشی از این اطلاعات همون شناسه مورد نظر ماست
    authority = req.json()['data']['authority']
    # print(authority)
    # در اینجا ما اومدیم براساس آبجکت کاربر یک جدول در جدول های مربوط به تراکتش ها ایجاد کردیم
    trans = Transactions()
    trans.user = request.user
    # در اینجا ما از اطلاعاتی که برامون ارسال شده شناسه درگاه رو بر میداریم و ذخیره میکنیم
    trans.authority = authority
    trans.amount = amount
    trans.save()

    if len(req.json()['errors']) == 0:
        resp["authority"] = authority
        resp["state"] = True
        resp["error"] = ""
        return JsonResponse(resp)
        # return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


# ........................//  comment //..............................
#.
# در اینجا بعد از انتقال کاربر به درگاه و اتمام عملیات کاربر به تابع verify درخواست فرستاده میشه
# و در این تابع بررسی میشه که وضعیت تراکنش به چه صورت هسنش
# .
# ........................//  comment //..............................


def verify(request):
    # در t_status ما از اطلاعات ارسالی درگاه وضعیت تراکنش رو میگیرم
    t_status = request.GET.get('Status')
    # در t_authority ما شناسه درگاه رو دریافت میکنیم همونی باهاش جدول درست کردیم تو بخش بالا
    t_authority = request.GET['Authority']
    if t_status == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}

        try:
            trans = Transactions.objects.get(authority=t_authority)
        except Transactions.DoesNotExist:
            return HttpResponse('Transaction Not Found')

        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                import datetime
                from cart.models import Cart
                from MYmethod.Tamam import num_sep
                from factor.models import Factors, FacotrProduct
                trans.state = 1
                trans.payment_date = datetime.datetime.now()
                # شماره تراکنش که به واسته اون و کاربر، ما فاکتور رو ایجاد میکنیم
                trans.ref_id = req.json()['data']['ref_id']
                trans.save()

                c = Cart.objects.filter(id_user=trans.user)

                # .........................//    شروع ایجاد فاکتور برای کاربر     //..................

                user_factor = Factors()
                # کاربری که تراکنش رو انجام داده
                user_factor.id_user = trans.user
                user_factor.payment_date = datetime.datetime.now()
                # کد پرداخت موفق برابر 1
                user_factor.state = 1
                user_factor.ref_id = req.json()['data']['ref_id']
                user_factor.creat_date = datetime.datetime.now()
                user_factor.save()
                # قیمت نهایی پس از وارد کردن محصولات در فاکتور ، در پایین وارد میشه

                # .........................//    پایان ایجاد فاکتور برای کاربر     //..................

                #.............................//  important point //...................................
                #.
                #  در اینجا ما باید یک رشته از فاکتور اصلی کاربر برای ساخت فکتور محصولات نیاز داریم
                # و برای بدست آوردن رشته مورد نظر هم از رشته کاربر استفاده می کنیم و هم از کد ref_id
                # چون یک کاربر ممکنه چندین فاکتور داشته باشه به
                # همین دلیل ما برای دریافت رشته مورد نظر هم از trans.user و هم ref_id استفاده کردیم
                #.
                #............................//  important point //....................................

                user_factor = Factors.objects.get(ref_id=req.json()['data']['ref_id'], id_user=trans.user)
                pro_list = []
                gheymat = total_price = 0
                for i in c:
                    #todo:
                    # please create factor from user's cart [FreezeMan]

                    # در اینجا چون کاربر هزینه محصول رو پرداخت کرده ، ما از قیمت واحدی (unit_price) که در سبد خرید
                    # ثبت شده استفاده میکنیم

                    show_price = num_sep(i.unit_price)
                    #  این i.total_price قیمت کل هر محصول هستش
                    show_total = num_sep(i.total_price)

                    # اطلاعات ریز محصولات در por_list قرار دادیم

                    pro_list.append([i.id_product.name, i.count, show_price, show_total, i.id_product.id,
                                     i.id_product.category.name])

                    # در اینجا قیمت کل هر محصول رو باهم جمع میکنیم تا قیمت نهایی بدس بیاد

                    total_price += i.total_price

                    # .........................//    شروع ایجاد فاکتور برای محصولات     //..................

                    prod_factors = FacotrProduct()
                    prod_factors.id_factor = user_factor
                    # موارد id_product ,count ,unit_price ,total_price  رو از سبد خرید دریافت کردیم
                    prod_factors.id_product = i.id_product
                    prod_factors.count = i.count
                    prod_factors.unit_price = i.unit_price
                    prod_factors.total_price = i.total_price
                    prod_factors.save()

                # متغییر gheymat مقداری عددی قیمت نهایی رو به قالب میفرسته
                # تا اگر جایی لازم بودم ازش استفاده بشه

                gheymat = total_price
                user_factor.total_price = gheymat
                user_factor.save()
                # متغییر total_price قیمت نهایی با جدا کننده رو  برای نمایش در فاکتور ارسال میکنه

                total_price = num_sep(total_price)

                #.........................//  default response in zarin pal //..........................
                #.
                # return HttpResponse('Transaction success.\nRefID: ' + str(
                #     req.json()['data']['ref_id'] ))
                #.
                #.........................//  default response in zarin pal //..........................

                context = {
                    "amount": trans.amount,
                    "pro": pro_list,
                    "total_price": total_price,
                    "show_sabad": gheymat,
                    "RefID": req.json()['data']['ref_id']
                }
                c.delete()
                return render(request, "cart/factor.html", context={"data": context})
            elif t_status == 101:

                #.............................//  important point //...................................
                #.
                # در اینجا تراکنش با موفقیت انجام شده و قبلا احراز تراکنش انجام شده
                # پس باید صرفا فاکتور نمایش داده بشه و هیچ موردی نیاز به تغییر در دیتابیس نداره
                # یعنی این تراکنش با کد 101 قبلا مرحله بالا یعنی کد 100 رو گذرونده
                #.
                #............................//  important point //....................................
                from cart.models import Cart
                from MYmethod.Tamam import num_sep, re100
                from factor.models import Factors, FacotrProduct
                try:
                    c = Cart.objects.filter(id_user=trans.user)
                    user_factor = Factors.objects.get(ref_id=req.json()['data']['ref_id'], id_user=trans.user)
                    pro_list = []
                    gheymat = total_price = 0
                    for i in c:
                        # در اینجا چون کاربر هزینه محصول رو پرداخت کرده ، ما از قیمت واحدی (unit_price) که در سبد خرید
                        # ثبت شده استفاده میکنیم

                        show_price = num_sep(i.unit_price)
                        #  این i.total_price قیمت کل هر محصول هستش
                        show_total = num_sep(i.total_price)

                        # اطلاعات ریز محصولات در por_list قرار دادیم

                        pro_list.append([i.id_product.name, i.count, show_price, show_total, i.id_product.id,
                                         i.id_product.category.name])

                        # در اینجا قیمت کل هر محصول رو باهم جمع میکنیم تا قیمت نهایی بدس بیاد

                        total_price += i.total_price
                    total_price = num_sep(total_price)
                    context = {
                        "amount": trans.amount,
                        "pro": pro_list,
                        "total_price": total_price,
                        "show_sabad": gheymat,
                        "RefID": req.json()['data']['ref_id']
                    }
                    c.delete()
                    return render(request, "cart/factor.html", context={"data": context})
                except Factors.DoesNotExist:
                    # در اینجا متد re100 در صورتی که فاکتوری برای کاربر ایجاد نشده بود
                    # براش فاکتور ایجاد میکنه
                    context = re100(req, t_authority)
                    return render(request, "cart/factor.html", context={"data": context})

                #.........................//  default response in zarin pal //..........................
                #.
                # return HttpResponse('Transaction submitted : ' + str(
                #     req.json()['data']['message']
                # ))
                #.
                #.........................//  default response in zarin pal //..........................
            else:
                import datetime
                trans.state = 0
                trans.payment_date = datetime.datetime.now()
                # trans.ref_id = req.json()['data']['ref_id']
                trans.save()
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return redirect("cart_home")
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            import datetime
            trans.state = 0
            trans.payment_date = datetime.datetime.now()
            # trans.ref_id = req.json()['data']['ref_id']
            trans.save()
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')