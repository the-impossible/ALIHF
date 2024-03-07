# My Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# My App imports


# Create your views here.
class HomeView(TemplateView):
    template_name = "frontend/home.html"
