from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
# Create your views here.


def index(request):
    return HttpResponse("account index")


def login(request):
    from .forms import Loginform
    if request.method == "POST":
        print(request.POST)
        from django.contrib.auth import authenticate, login
        form = Loginform(request.POST or None)
        # در  اینجا ما بررسی میکنیم اطلاعات برای ما ارسال شده یا نه
        if form.is_valid():
            username = form.cleaned_data["User_name"]
            password = form.cleaned_data["Password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard_home")
            else:
                return render(request, "account/login2.html", {"form": form})
            # در اینجا ما خطا ها رو ارسال میکنیم به قالب برای render شدن
        return render(request, "account/login2.html", {"form": form})
    elif request.method == "GET":
        if request.user and request.user.is_authenticated:
            lo = 1
            return redirect("products_home", {"login": lo})
        else:
            lo = 0
            form = Loginform()
        return render(request, "account/login2.html", {"login": lo, "form": form})
    else:
        return Http404()


def logout(request):
    from django.contrib.auth import logout
    if request.user.is_authenticated:
        logout(request)
        return redirect("account_login")


def register(request):
    from .forms import RegisterForm
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            from django.contrib.auth.models import User
            first_name = form.cleaned_data["First_name"]
            lastname = form.cleaned_data["Last_name"]
            username = form.cleaned_data['User_name']
            email = form.cleaned_data['Email']
            password = form.cleaned_data["Password"]
            # password = form.cleaned_data.get("passw")
            # mishe get bezani tuple begiri ia nazani list begiri
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = lastname
            user.save()
            return redirect('account_login')
        # در اینجا در صورتی که تو بخش is_valid خطایی رخ بده تو context ارسالی به قالب
        # خطاهای رخ داده توی فرم ارسال میشه و قالب دوباره render میشه
        # و در این سری خطاهای فرم در قالب نمایش داده میشه
        return render(request, 'account/register2.html', {'form': form})
    elif request.method == 'GET':

        # در اینجا وقتی کاربر وارد صفحه ثبت نام میشه یه فرم خالی براش ایجاد میشه
        # و به عنوان context به قالب ارسال میشه و حین render نمایش داده میشه
        form = RegisterForm()
        return render(request, 'account/register2.html', {'form': form})
    else:
        return Http404


#..........................// مهرشاد تو باید حتما مستقل بشی //.............................
#.............................// マーシャッドあなたは独立している必要があります //.............................


def profile(request):
    return render(request, "account/../Template/profile/profile.html")
