from django.urls import path
from ALIHF_basic.views import *

app_name = "basic"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
]
