from django.shortcuts import render, redirect  # redirectt重新導入
from django.http import HttpResponse  # 封裝套件
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
# 功能都在這寫


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    user = request.user
    return render(request, "user/profile.html", {"user": user})


def user_login(request):
    message = ""
    if request.method == "POST":
        if request.POST.get("register"):
            return redirect("register")  # 這邊不一樣在哪
        elif request.POST.get("login"):
            username = request.POST["username"]
            password = request.POST["password"]
            user = User.objects.filter(username=username)

            if not user:
                message = "無此帳號!"
            else:
                user = authenticate(request, username=username, password=password)
                if not user:
                    message = "密碼錯誤!"
                else:
                    login(request, user)
                    message = "登入成功!"
                    # return redirect("profile")
                    return redirect("todo")

            print(user)
        # if username in User.objects.filter():
        #     print(User.objects.filter("username"))

    return render(request, "user/login.html", {"message": message})


def register(request):
    message = ""
    # return HttpResponse("<h1>Hello Django!</h1>")  # HttpResponse封裝
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            message = "輸入密碼不相同!"
        elif len(password1) < 8:
            message = "密碼不得小於8個字元!"
        else:
            # 確認帳號是否重複
            if User.objects.filter(username=username):
                message = "帳號重複!"
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save
                message = "註冊成功!"
                return redirect("login")

    form = UserCreationForm()
    return render(request, "user/register.html", {"form": form, "message": message})
