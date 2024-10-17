from decouple import config

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS").split(",")

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS").split(",")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-api-key",
]

CORS_EXPOSE_HEADERS = [
    "x-custom-header",
]
CORS_ALLOW_CREDENTIALS = True


CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"


CORS_ALLOW_METHODS += [
    "HEAD",
]

CORS_ALLOW_HEADERS += [
    "x-admin-custom-header",
]