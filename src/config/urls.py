from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("tickets/", include("apps.core.urls")),
    path("exchange_rates/", include("apps.exchange_rates.urls")),
]
