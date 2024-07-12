from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *
from app02.utils.bootstrap import BootStrapModelForm
from app02.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="confirm password", widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {"password": forms.PasswordInput(render_value=True)}

    def clean_password(self):
        pswd = self.cleaned_data.get("password")
        return md5(pswd)

    def clean_confirm_password(self):
        # print(self.cleaned_data)
        pswd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pswd != confirm:
            raise ValidationError(message="Passwords do not match, please re-enter")
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="confirm password", widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]

    def clean_password(self):
        pswd = self.cleaned_data.get("password")
        md5_pswd = md5(pswd)
        exists = models.Admin.objects.filter(
            id=self.instance.pk, password=md5_pswd
        ).exists()
        if exists:
            raise ValidationError("Password cannot be the same as the previous one")
        return md5(pswd)

    def clean_confirm_password(self):
        # print(self.cleaned_data)
        pswd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pswd != confirm:
            raise ValidationError(message="Passwords do not match, please re-enter")
        return confirm


def admin_list(request):

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset=queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data,
    }
    return render(request, "admin_list.html", context)


def admin_add(request):
    title = "New Administrator"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, "error.html", {"msg": "Page Not Found"})
    title = "Edit Admin"

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)

        return render(request, "change.html", {"title": title, "form": form})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).first().delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")
    title = "Reset password for {}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})
