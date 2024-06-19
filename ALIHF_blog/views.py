from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.text import slugify

from ALIHF_blog.models import *

# Create your views here.

class PostDetailView(DetailView):
    model = BlogPost
    template_name = "frontend/post_details.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['recent'] = BlogPost.objects.exclude(blog_id__exact=context['object'].blog_id)[:3]
        return context