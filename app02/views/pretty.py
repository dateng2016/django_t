from django.shortcuts import render, redirect
from app02 import models
from app02.utils.pagination import Pagination
from app02.utils.form import *


def pretty_list(request):
    # for i in range(300):
    #     models.PrettyNum.objects.create(
    #         mobile="11111111111", price=10, level=1, status=1
    #     )

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")

    page_object = Pagination(request, queryset)
    page_string = page_object.html()

    return render(
        request,
        "pretty_list.html",
        {
            "queryset": page_object.page_queryset,
            "search_data": search_data,
            "page_string": page_string,
        },
    )

    # page = int(request.GET.get("page", 1))
    # page_size = 10
    # start = (page - 1) * page_size
    # end = page * page_size

    # page_queryset = page_object.page_queryset

    # # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")[
    # #     page_object.start : page_object.end
    # # ]

    # obj_count = models.PrettyNum.objects.filter(**data_dict).count()
    # page_count, div = divmod(obj_count, page_size)
    # if div:
    #     page_count += 1

    # plus = 5
    # if page_count <= 2 * plus + 1:
    #     start_page = 1
    #     end_page = page_count
    # else:
    #     if page <= plus:
    #         start_page = 1
    #         end_page = 2 * plus + 1
    #     else:
    #         if (page + plus) > page_count:
    #             start_page = page_count - 2 * plus
    #             end_page = page_count
    #         else:
    #             start_page = page - plus
    #             end_page = page + plus

    # page_str_list = []

    # page_str_list.append('<li><a href="?page=1">First Page</a></li>')

    # if page > 1:
    #     prev = '<li><a href="?page={}">Prev</a></li> '.format(page - 1)
    #     page_str_list.append(prev)

    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li> '.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li> '.format(i, i)
    #     page_str_list.append(ele)

    # if page < page_count:
    #     nxt = '<li><a href="?page={}">Next</a></li> '.format(page + 1)
    #     page_str_list.append(nxt)

    # page_str_list.append('<li><a href="?page={}">Last Page</a></li>'.format(page_count))

    # search_string = """
    #         <li>
    #             <form style="float: left;margin-left: -1px" method="get">
    #                 <input name="page"
    #                        style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
    #                        type="text" class="form-control" placeholder="Page">
    #                 <button style="border-radius: 0" class="btn btn-default" type="submit">Go</button>
    #             </form>
    #         </li>
    #         """

    # page_str_list.append(search_string)

    # page_string = "".join(page_str_list)


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
