from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ALIHF_basic.urls", namespace="basic")),
    path("", include("ALIHF_auth.urls", namespace="auth"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "African Leader in Health Fellowship"
admin.site.site_title = "African Leader in Health Fellowship"
admin.site.index_title = "Welcome to African Leader in Health Fellowship"