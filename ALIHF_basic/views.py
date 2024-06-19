# My Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# My App imports
from ALIHF_blog.models import *

# Create your views here.
class HomeView(ListView):
    model = BlogPost
    template_name = "frontend/home.html"

    def get_queryset(self):
        return BlogPost.objects.all()

class AboutView(TemplateView):
    template_name = "frontend/about.html"

class ContactView(TemplateView):
    template_name = "frontend/contact.html"
