from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from django.shortcuts import redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request: HttpRequest):
        # print("Auth. Welcome")
        if request.path_info in ["/login/", "/image/code/"]:
            return
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect("/login/")

    def process_response(self, request, response):
        # print("Auth, Bye")
        return response
