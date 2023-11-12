from django.shortcuts import render
from django.http import HttpResponse  # 封裝套件

# Create your views here.
# 功能都在這寫


def register(request):
    # return HttpResponse("<h1>Hello Django!</h1>")  # HttpResponse封裝
    return render(request, "user/register.html")
