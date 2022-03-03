from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
# Create your views here.


def index(request):
    return HttpResponse("account index")


def login(request):
    #return (request.method)
    if request.method == "POST":
        print(request.POST)
        from django.contrib.auth import authenticate, login
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard_home")
        else:
            return render(request, "account/login.html", {"error": "Auth Failed"})
        # return HttpResponse("post")
    elif request.method == "GET":
        if request.user and request.user.is_authenticated:
            lo = 1
            return redirect("products_home",{"login": lo})
        else:
            lo = 0
        return render(request, "account/login.html", {"login": lo})
    else:
        return Http404()


def logout(request):
    from django.contrib.auth import logout
    if request.user.is_authenticated:
        logout(request)
        return redirect("account_login")


def register(request):
    if request.method == "POST":
        from django.contrib.auth.models import User

        username = request.POST.get("username", None)
        fullname = request.POST.get("fullname", None)
        if None not in [username, fullname]:
            if isinstance(fullname, str) and fullname.index(" ") > 0:
                first_name, lastname = fullname.split()
            else:
                first_name = lastname = ""
        else:
            return render(request, "account/register.html", {"error": "اطلاعات را به طور کامل وارد نمایید1"})
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        if None not in [username, lastname, password, email]:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = lastname
            user.save()
            return redirect("account_login")
        else:
            return render(request, "account/register.html", {"error": "اطلاعات را به طور کامل وارد نمایید شسشس2"})
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect("dashboard_home")
        else:
            return render(request, "account/register.html")
    else:
        return Http404()


def profile(request):
    return HttpResponse("account profile")
