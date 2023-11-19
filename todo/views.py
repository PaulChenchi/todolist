from django.shortcuts import render, HttpResponse
from .models import Todo

# Create your views here.

# 登入=>首頁
# 如果沒有代辦事項==>提示無代辦事項
# 重要代辦事項顯示紅色


def todo(request):
    # all,filter,get
    user = request.user
    todos = None
    # if todos == None:
    #     # return HttpResponse("目前無代辦事項")
    #     return render(request, "todo/todo.html", {"todos": todos})
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)
        print(todos)
    return render(request, "todo/todo.html", {"todos": todos})
