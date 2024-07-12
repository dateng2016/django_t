from app02 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3)

    class Meta:
        model = models.UserInfo
        fields = [
            "name",
            "password",
            "age",
            "account",
            "create_time",
            "gender",
            "depart",
        ]

        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


class PrettyModelForm(forms.ModelForm):
    # Method 1 for Validation
    # mobile = forms.CharField(
    #     validators=[RegexValidator(r"^1[3-9]\d{9}$", "Wrong Format Phone Number")]
    # )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"
        # exclude = ["level"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    # Method 2 for valideation
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("Phone number already exists")
        if len(txt_mobile) != 11:
            raise ValidationError("Wrong Format")
        return txt_mobile


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True)
    mobile = forms.CharField(
        validators=[RegexValidator(r"^1[3-9]\d{9}$", "Wrong Format Phone Number")]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"
        # exclude = ["level"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):
        print(f"Here is the primary key {self.instance.pk}")

        txt_mobile = self.cleaned_data["mobile"]
        exists = (
            models.PrettyNum.objects.exclude(id=self.instance.pk)
            .filter(mobile=txt_mobile)
            .exists()
        )
        if exists:
            raise ValidationError("Phone number already exists")
        if len(txt_mobile) != 11:
            raise ValidationError("Wrong Format")
        return txt_mobile
