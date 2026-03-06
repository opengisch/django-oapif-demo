import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

LOGINS = {
    os.getenv("DJANGO_SUPERUSER_USERNAME"): os.getenv("DJANGO_SUPERUSER_PASSWORD"),
    os.getenv("DJANGO_READONLY_USER_USERNAME"): os.getenv(
        "DJANGO_READONLY_USER_PASSWORD"
    ),
    os.getenv("DJANGO_READWRITE_USER_USERNAME"): os.getenv(
        "DJANGO_READWRITE_USER_PASSWORD"
    ),
}


def dowload_qgs_auth(request):
    password = LOGINS.get(request.user.username, None)
    print(password)
    if password is None:
        messages.error(request, "Can't generate authentication file for user")
        return redirect("admin:index")
    context = {
        "username": request.user.username,
        "password": password,
    }
    res = render_to_string("qgis/auth.xml", context)
    return HttpResponse(res, content_type="application/xml")
