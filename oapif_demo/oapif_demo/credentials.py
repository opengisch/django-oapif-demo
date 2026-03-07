import os

from django.http import HttpRequest

LOGIN_CREDENTIALS = {
    os.getenv(f"DJANGO_{user}_USERNAME"): os.getenv(f"DJANGO_{user}_PASSWORD")
    for user in ("SUPERUSER", "READONLY_USER", "READWRITE_USER")
}


def context_processor(request: HttpRequest):
    return {"LOGIN_CREDENTIALS": LOGIN_CREDENTIALS}
