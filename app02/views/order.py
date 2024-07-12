import json
from io import BytesIO
from random import randint
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt


from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *
from app02.utils.bootstrap import *


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request: HttpRequest):
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, "order_list.html", context=context)


@csrf_exempt
def order_add(request: HttpRequest):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(
            randint(1000, 9999)
        )
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request: HttpRequest):
    uid = request.GET.get("uid")
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request: HttpRequest):
    # uid = request.GET.get("uid")
    # print(uid)
    # row_object = models.Order.objects.filter(id=uid).first()
    # if not row_object:
    #     return JsonResponse({"status": False, "error": "Not Found"})
    # result = {
    #     "status": True,
    #     "data": {
    #         "title": row_object.title,
    #         "price": row_object.price,
    #         "status": row_object.status,
    #     },
    # }
    # return JsonResponse(result)
    uid = request.GET.get("uid")
    print(uid)
    row_dict = (
        models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    )
    print(row_dict)
    result = {"status": True, "data": row_dict}
    return JsonResponse(result)


@csrf_exempt
def order_edit(request: HttpRequest):
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "Not Found"})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
