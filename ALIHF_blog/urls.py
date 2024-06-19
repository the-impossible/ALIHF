from django.urls import path
from ALIHF_blog.views import *

app_name = "blog"

urlpatterns = [
    path('post_details/<slug>', PostDetailView.as_view(), name='post_details'),
]
