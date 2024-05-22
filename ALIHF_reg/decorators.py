# My django imports
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

# My app imports

# Determining if the user is an admin
def has_updated(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.has_updated():
            return func(request, *args, **kwargs)
        else:
            messages.info(request, 'You have to update your profile image before proceeding!')
            return redirect('auth:profile', request.user.user_id)
    return wrapper_func
