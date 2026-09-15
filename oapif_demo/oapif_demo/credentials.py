import os

from django.conf import settings
from django.http import HttpRequest

LOGIN_CREDENTIALS = {
    os.getenv(f"DJANGO_{user}_USERNAME"): os.getenv(f"DJANGO_{user}_PASSWORD")
    for user in ("SUPERUSER", "READONLY_USER", "READWRITE_USER")
}

def context_processor(request: HttpRequest):
    if settings.DEBUG:
        return { "LOGIN_CREDENTIALS": LOGIN_CREDENTIALS }

    credentials = LOGIN_CREDENTIALS.copy()
    del credentials[os.getenv("DJANGO_SUPERUSER_USERNAME")]
    return {"LOGIN_CREDENTIALS": credentials}

