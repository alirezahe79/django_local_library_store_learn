from django.contrib.auth.models import User


def GlobalModels(request):
    from cart.models import Cart

    user = request.user
    c_count = 0
    if user and user.is_authenticated:
        c = Cart.objects.filter(id_user=user)
        for i in c:
            # در اینجا ما از رشته سبد ، آبجکت محصول رو درآوردیم تا به نام و قیمت محصول بررسیم
            c_count += i.count
            # pro_list.append([i.id_product.name, i.count, i.unit_price, i.total_price, i.id_product.id])
    return {"cart": c_count}
