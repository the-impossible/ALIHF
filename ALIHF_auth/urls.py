from django.urls import path
from ALIHF_auth.views import *

app_name = "auth"

urlpatterns = [
    path('login', LoginPageView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('reset_password', ResetPasswordPageView.as_view(), name='reset_password'),
    path('reset_password_activation/<uidb64>/<token>', ResetPasswordActivationView.as_view(), name='reset_password_activation'),


    path('register', RegisterPageView.as_view(), name='register'),
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
    path('auth/profile/<str:pk>',
         UpdateProfileView.as_view(), name='profile'),

    path('test_email', TestEmailView.as_view(), name='test_email'),
]
