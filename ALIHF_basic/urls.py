from django.urls import path
from ALIHF_basic.views import *

app_name = "basic"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
