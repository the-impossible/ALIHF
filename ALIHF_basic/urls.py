from django.urls import path
from ALIHF_basic.views import *

app_name = "basic"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('webinars', WebinarsView.as_view(), name='webinars'),
    path('survey_details/<str:pk>', WebinarSurveyDetailView.as_view(), name='survey_details'),

]
