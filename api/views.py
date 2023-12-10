from django.shortcuts import render, HttpResponse
from todo.models import Todo
import json
from datetime import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


# 取得所有代辦事項

# {
#   success:True,
# data:[
#     {
#             id:xxxx,
#             title:xxxx,
#     },
# ]
# }


def convert_date(date, format="%Y-%m-%d %H:%M:%S"):
    try:
        return date.strftime(format)
    except Exception as e:
        print(e)
    return None


@csrf_exempt
def delete_todo_api(request, id):
    success = True
    if request.method == "DELETE":
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()

            message = {
                "success": success,
                "todo_id": id,
                "message": "刪除資料成功",
            }

        except Exception as e:
            print(e)
            success = False
            message = {"success": success, "message": str(e)}
        response_data = json.dumps(message, ensure_ascii=False)  # 組成json格式
        return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
def update_todo_api(request, id):
    success = True
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            todo = Todo.objects.get(id=id)
            user = (
                User.objects.get(username=data.get("user"))
                if data.get("user")
                else todo.user
            )

            # if data.get("user"):
            #     user = User.objects.get(username=data.get("user"))
            # else:
            #     user=todo.user

            todo.title = data.get("title", todo.title)
            todo.text = data.get("text", todo.text)
            todo.date_completed = data.get("date_completed", todo.date_completed)
            todo.important = data.get("important", todo.important)
            todo.completed = data.get("completed", todo.completed)

            todo.user = user
            todo.save()

            message = {
                "success": success,
                "todo_id": todo.id,
                "message": "更新資料成功",
            }

        except Exception as e:
            print(e)
            success = False
            message = {"success": success, "message": str(e)}
        response_data = json.dumps(message, ensure_ascii=False)  # 組成json格式
        return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
def add_todo_api(request):
    success = True
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data.get("user"))
            todo = Todo.objects.create(
                title=data.get("title"),
                text=data.get("text"),
                date_completed=data.get("date_completed"),
                important=data.get("important"),
                completed=data.get("completed"),
                user=user,
            )
            message = {
                "success": success,
                "todo_id": todo.id,
                "title": todo.title,
                "username": user.username,
            }

        except Exception as e:
            print(e)
            success = False
            message = {"success": success, "message": str(e)}
        response_data = json.dumps(message, ensure_ascii=False)  # 組成json格式
        return HttpResponse(response_data, content_type="application/json")


def user_api(request, id):
    user_list = []
    success = True
    message = ""
    try:
        users = User.objects.all()
        for user in users:
            user_list.append(
                {
                    "id": user.id,
                    "password": user.password,
                    "last_login": convert_date(user.last_login),
                    "is_superuser": user.is_superuser,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_active": user.is_active,
                    "date_joined": convert_date(user.date_joined),
                }
            )
    except Exception as e:
        print(e)
        message = str(e)
    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": user_list,
        "message": message,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")


def users_api(request):
    user_list = []
    success = True
    message = ""
    try:
        users = User.objects.all()
        for user in users:
            user_list.append(
                {
                    "id": user.id,
                    "password": user.password,
                    "last_login": convert_date(user.last_login),
                    "is_superuser": user.is_superuser,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_active": user.is_active,
                    "date_joined": convert_date(user.date_joined),
                }
            )
    except Exception as e:
        print(e)
        message = str(e)
    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": user_list,
        "message": message,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")


# get/all/filter
def user_todos_api(request, id):
    todo_list = []
    success = True
    message = ""
    try:
        user = User.objects.get(id=id)
        todos = Todo.objects.filter(user=user)
        for todo in todos:
            todo_list.append(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "text": todo.text,
                    "created": convert_date(todo.created),
                    "date_completed": convert_date(todo.date_completed),
                    "important": todo.important,
                    "completed": todo.completed,
                    "user": {"name": todo.user.username, "email": todo.user.email},
                }
            )
    except Exception as e:
        print(e)
        message = str(e)
        success = False
    # 輸出格式
    # {'success':true,'request_date':'2023-12-10','data':[]}
    #
    print(todo_list)
    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": todo_list,
        "message": message,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")


# .all().get()
def todo_api(request, id):
    success = True
    todo = None
    message = ""
    try:
        todo = Todo.objects.get(id=id)
        todo = {
            "id": todo.id,
            "title": todo.title,
            "text": todo.text,
            "created": convert_date(todo.created),
            "date_completed": convert_date(todo.date_completed),
            "important": todo.important,
            "completed": todo.completed,
            "user": {"name": todo.user.username, "emil": todo.user.email},
        }
    except Exception as e:
        print(e)
        message = "id編號不正確"
        success = False

    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": todo,
        "message": message,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")


def todos_api(request):
    todo_list = []
    success = True
    try:
        todos = Todo.objects.all()
        for todo in todos:
            todo_list.append(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "text": todo.text,
                    "created": convert_date(todo.created),
                    "date_completed": convert_date(todo.date_completed),
                    "important": todo.important,
                    "completed": todo.completed,
                    "user": {"name": todo.user.username, "email": todo.user.email},
                }
            )
    except Exception as e:
        print(e)
        success = False
    # 輸出格式
    # {'success':true,'request_date':'2023-12-10','data':[]}
    #
    print(todo_list)
    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": todo_list,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")
