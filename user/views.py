from django.shortcuts import render
from django.http import HttpResponse  # 封裝套件
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
# 功能都在這寫


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

    form = UserCreationForm()
    return render(request, "user/register.html", {"form": form, "message": message})
