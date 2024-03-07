from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("gym-api/", include("gym_api.urls", namespace="gym")),
    path("auth/", include("user.urls", namespace="auth")),
    path("__debug__/", include("debug_toolbar.urls")),

    path("docs/", SpectacularAPIView.as_view(), name="docs"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="docs"), name="swagger"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="docs"), name="redoc"),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
