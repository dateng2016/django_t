from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import render, redirect, HttpResponse

from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *
from app02.utils.bootstrap import *
from app02.utils.encrypt import md5
from app02.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
        required=True,
    )

    code = forms.CharField(widget=forms.TextInput, required=True)

    def clean_password(self):
        pswd = self.cleaned_data.get("password")
        return md5(pswd)


def login(request: HttpRequest):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Wrong Verification Code")
            return render(request, "login.html", {"form": form})

        print(form.cleaned_data)
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "Wrong Username or Password")
            return render(request, "login.html", {"form": form})

        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list/")
    return render(request, "login.html", {"form": form})


def logout(request: HttpRequest):
    request.session.clear()
    return redirect("/login/")


def image_code(request: HttpRequest):
    img, code_string = check_code()
    request.session["image_code"] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())
