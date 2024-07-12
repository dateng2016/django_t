from django.shortcuts import render, HttpResponse, redirect
from app01.models import Department, UserInfo

# Create your views here.


def index(request):
    return HttpResponse("Hello World")


def user_list(request):
    # 1.Upon configuration:
    # It will look for the templates directory
    # in the root directory then go through the app directories one by one
    # 2. By default:
    # Looks for the user_list.html file in the app/templates
    # (according to the order of apps being registered within
    # the settings.py file, go through their templates one by one)
    return render(request, "user_list.html")


def user_add(request):
    return render(request, "user_add.html")


def tpl(request):
    name = "John Doe"
    roles = ["Admin", "CEO", "Security Guard"]
    user_info = {"name": "John Wack", "salary": 100000, "role": "CTO"}

    data_list = [
        {"name": "John Wack", "salary": 100000, "role": "CTO"},
        {"name": "John Doe", "salary": 100000, "role": "CTO"},
        {"name": "John Haha", "salary": 100000, "role": "CTO"},
    ]
    return render(
        request, "tpl.html", {"n1": name, "n2": roles, "n3": user_info, "n4": data_list}
    )


def news(request):

    return render(request, "news.html")


def something(request):

    print(request.method)

    print(request.GET)

    print(request.POST)

    # return HttpResponse("Return Content")

    # This has to be an absolute address
    return redirect("https://www.google.com/")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    # print(request.POST)
    username = request.POST.get("user")
    password = request.POST.get("pswd")
    if username == "root" and password == "123":
        # return HttpResponse("Login Successful")
        return redirect("https://amazon.com")
    # return HttpResponse("Login Failed")
    # return render(request, "login.html")
    return render(request, "login.html", {"error_msg": "Login Failed"})


def orm(request):
    """Testing ORM Operations"""

    # Department.objects.create(title="Sales")
    # Department.objects.create(title="IT")
    # Department.objects.create(title="DevOps")

    # UserInfo.objects.create(name="John Doe", password="123", age=1)
    # UserInfo.objects.create(name="Jane Wick", password="456", age=2)
    # UserInfo.objects.create(name="xiaoming", password="222")

    # UserInfo.objects.filter(id=3).delete()
    # Department.objects.all().delete()

    # datalist = UserInfo.objects.all()
    # for obj in datalist:
    #     print(obj.id, obj.name, obj.password, obj.age)

    # datalist = UserInfo.objects.filter(id=1)
    # print(datalist)
    # print(datalist[0].name)

    # data = UserInfo.objects.filter(id=1).first()
    # print(data)
    # print(data.name)

    # UserInfo.objects.all().update(password=999)
    # UserInfo.objects.filter(id=2).update(password=111)

    return HttpResponse("Success")


def info_list(request):
    # Get all information about users in the database
    data_list = UserInfo.objects.all()

    return render(request, "info_list.html", {"data_list": data_list})


def info_add(request):
    if request.method == "GET":
        return render(request, "info_add.html")
    user = request.POST.get("user")
    pswd = request.POST.get("pswd")
    age = request.POST.get("age")
    print(user, pswd, age)

    UserInfo.objects.create(name=user, password=pswd, age=age)

    return redirect("/info/list/")


def info_delete(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/info/list/")
