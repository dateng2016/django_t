from django.shortcuts import render, redirect
from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *


def user_list(request):
    if request.method == "GET":
        queryset = models.UserInfo.objects.all()
        # for obj in queryset:
        #     print(
        #         f" This is the ID: {obj.depart_id}"
        #     )  # the actual ID stored in the database
        #     print(f" This is the title: {obj.depart.title}")  # the depart title
        #     print(f"Created at: {obj.create_time}")

        page_object = Pagination(request, queryset)
        context = {
            "queryset": page_object.page_queryset,
            "page_string": page_object.html(),
        }

        return render(request, "user_list.html", context=context)


def user_add(request):
    if request.method == "GET":
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all(),
        }
        return render(request, "user_add.html", context)
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    ctime = request.POST.get("ctime")
    gender = request.POST.get("gd")
    depart_id = request.POST.get("dp")

    # 添加到数据库中
    models.UserInfo.objects.create(
        name=user,
        password=pwd,
        age=age,
        account=account,
        create_time=ctime,
        gender=gender,
        depart_id=depart_id,
    )

    # 返回到用户列表页面
    return redirect("/user/list/")


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # Get the row to edit from the database based on the nid
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")
