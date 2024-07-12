import json
from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt


from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *
from app02.utils.bootstrap import *


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {"detail": forms.TextInput}


def task_list(request: HttpRequest):
    queryset = models.Task.objects.all().order_by("-id")
    page_object = Pagination(request=request, queryset=queryset)

    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request: HttpRequest):
    print(request.GET)
    print(request.POST)

    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    # data_dict = {"status": True, "data": [11, 22, 33, 44]}
    # json_string = json.dumps(data_dict)

    data_dict = {"status": False, "error": form.errors}
    # return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
    return JsonResponse(data_dict)
