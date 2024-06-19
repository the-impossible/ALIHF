from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ALIHF_basic.urls", namespace="basic")),
    path("", include("ALIHF_auth.urls", namespace="auth")),
    path("", include("ALIHF_reg.urls", namespace="reg")),
    path("", include("ALIHF_blog.urls", namespace="blog")),

    # CKEditor
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "International Institute of Healthcare Leadership and Quality Assurance"
admin.site.site_title = "International Institute of Healthcare Leadership and Quality Assurance"
admin.site.index_title = "Welcome to International Institute of Healthcare Leadership and Quality Assurance"