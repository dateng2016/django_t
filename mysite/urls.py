"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path, re_path

# from app01 import views
# from app02 import views
from app02.views import depart, user, pretty, admin, account, task, order, upload

urlpatterns = [
    # path("admin/", admin.site.urls),
    # APP01
    # path("index/", views.index),
    # path("user/list/", views.user_list),
    # path("user/add/", views.user_add),
    # path("tpl/", views.tpl),
    # path("news/", views.news),
    # path("something/", views.something),
    # path("login/", views.login),
    # path("orm/", views.orm),
    # # Example, user management
    # path("info/list/", views.info_list),
    # path("info/add/", views.info_add),
    # path("info/delete/", views.info_delete),
    # APP02
    # Department Management
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),
    path("depart/<int:nid>/edit/", depart.depart_edit),
    path("depart/multi/", depart.depart_multi),
    # User Management
    path("user/list/", user.user_list),
    path("user/add/", user.user_add),
    path("user/model/form/add/", user.user_model_form_add),
    path("user/<int:nid>/edit/", user.user_edit),
    path("user/<int:nid>/delete/", user.user_delete),
    # Pretty Numbers
    path("pretty/list/", pretty.pretty_list),
    path("pretty/add/", pretty.pretty_add),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete),
    # Admin
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/edit/", admin.admin_edit),
    path("admin/<int:nid>/delete/", admin.admin_delete),
    path("admin/<int:nid>/reset/", admin.admin_reset),
    # Login
    path("login/", account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),
    # Task
    path("task/list/", task.task_list),
    path("task/ajax/", task.task_ajax),
    # Order
    path("order/list/", order.order_list),
    path("order/add/", order.order_add),
    path("order/delete/", order.order_delete),
    path("order/detail/", order.order_detail),
    path("order/edit/", order.order_edit),
    # Upload
    path("upload/list/", upload.upload_list),
    path("upload/form/", upload.upload_form),
]
