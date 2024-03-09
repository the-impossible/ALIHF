# My Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# My App imports


# Create your views here.
class LoginPageView(TemplateView):
    template_name = "backend/auth/login.html"

class RegisterView(TemplateView):
    template_name = "backend/auth/register.html"
