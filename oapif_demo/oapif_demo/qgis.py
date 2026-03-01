"""
URL configuration for oapif_demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

import os
from pathlib import Path

from django.conf import settings
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

SERVER_DOMAIN = os.getenv("CADDY_DOMAIN")
SERVER_PROTOCOL = "http" if settings.DEBUG else "https"


def generate_qgs_project():
    dev_qgs = Path(f"{settings.STATIC_ROOT}/qgis/bees_dev.qgs").read_text()
    qgs = dev_qgs.replace(
        "https://localhost/oapif",
        f"{SERVER_PROTOCOL}://{SERVER_DOMAIN}/oapif",
    )
    Path(f"{settings.STATIC_ROOT}/qgis/bees.qgs").write_text(qgs)


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
