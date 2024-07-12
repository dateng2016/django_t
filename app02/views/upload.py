import os
import json
from io import BytesIO
from random import randint
from datetime import datetime

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms


from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *
from app02.utils.bootstrap import *


def upload_list(request: HttpRequest):
    if request.method == "GET":
        return render(request, "upload_list.html")
    print(f"Here is the post")
    print(request.POST)
    print(request.FILES)
    file_object = request.FILES.get("avatar")
    print(file_object.name)
    with open(file_object.name, "wb") as f:
        for chunk in file_object.chunks():
            f.write(chunk)

    return HttpResponse("Success")


class UpForm(BootStrapForm):
    name = forms.CharField()
    age = forms.IntegerField()
    img = forms.FileField()


def upload_form(request: HttpRequest):
    title = "Form Upload"
    if request.method == "GET":
        form = UpForm()
        return render(request, "upload_form.html", {"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        image_object = form.cleaned_data.get("img")
        # file_path = "app02/static/img/{}".format(image_object.name)
        file_path = os.path.join("app02", "static", "img", image_object.name)
        with open(file_path, "wb") as f:
            for chunk in image_object.chunks():
                f.write(chunk)
            models.Boss.objects.create(
                name=form.cleaned_data.get("name"),
                age=form.cleaned_data.get("age"),
                img=file_path,
            )
        return HttpResponse("Success")
    return render(request, "upload_form.html", {"form": form, "title": title})
