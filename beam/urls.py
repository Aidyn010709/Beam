from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Beam Post",
        default_version="v1",
        description="Kyrgyz Post web API version 1",
    ),
    public=True,
)

urlpatterns = [
    path("beam-admin-panel/secret/", admin.site.urls),
    path('user/', include("applications.user.urls")),
    path('network/', include("applications.network.urls")),
    path('products/', include("applications.product.urls")),
    path('cart/', include("applications.cart.urls")),
    path('payment/', include("applications.payment.urls")),
]
urlpatterns += [path("i18n/", include("django.conf.urls.i18n"))]
urlpatterns += i18n_patterns(
    path("beam-admin-panel/secret/", admin.site.urls)
)
admin.site.site_header = "Beam Service"
admin.site.index_title = "Administration"
admin.site.site_title = "Beam Platform"


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DJANGO_ENV == "local" or settings.DJANGO_ENV == "dev":
    from django.contrib.auth.decorators import login_required

    urlpatterns += [
        path(
            "my-swagger-documents-for-frontend/",
            login_required(schema_view.with_ui("swagger", cache_timeout=0)),
            name="swagger-ui",
        ),
    ]
