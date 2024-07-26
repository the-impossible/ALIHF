# My Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# My App imports
from ALIHF_blog.models import *
from ALIHF_basic.models import *
from ALIHF_reg.models import *

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

class WebinarsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = WebinarVideos.objects.all().order_by('-date_created')
        context["survey_list"] = WebinarSurveys.objects.all().order_by('-date_created')
        return context

    template_name = "frontend/webinars.html"

class WebinarSurveyDetailView(DetailView):
    model = WebinarSurveys
    template_name = "frontend/survey_details.html"