from django.urls import path
from ALIHF_auth.views import *

app_name = "auth"

urlpatterns = [
    path('login', LoginPageView.as_view(), name='login'),
    path('register', RegisterPageView.as_view(), name='register'),
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
]
