# My Django imports
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy

# My App imports
from ALIHF_auth.models import *
from ALIHF_auth.forms import *
from ALIHF_auth.utils import *

#Email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError


# Create your views here.
class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LoginPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user.name}")

                    nxt = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(
                        request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(
            request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')

class RegisterPageView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/register.html"
    success_message = "Registration Successful you can now login"

    def get_success_url(self):
        return reverse("auth:login")

    def form_valid(self, form):

        # SEND EMAIL
        user_details = {
            'name':form.cleaned_data['name'],
            'email':form.cleaned_data['email'],
            'domain': get_current_site(self.request).domain,
        }

        Email.send(user_details, 'welcome')
        return super().form_valid(form)

class UpdateProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "backend/profile.html"
    form_class = UpdateUserCreationForm
    success_message = 'Account Updated Successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Update'
        return context

class ResetPasswordPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/reset_password.html')

    def post(self, request):
        email = request.POST.get('email').lower()
        if email:
            user = User.objects.filter(email=email)
            if user.exists():
                current_site = get_current_site(request).domain
                data = user[0]
                user_details = {
                    'name':data.name,
                    'email': data.email,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(data.user_id)),
                    'token': email_activation_token.make_token(data),
                }
                Email.send(user_details, 'reset')
                messages.success(request, 'A mail has been sent to your mailbox to enable you reset your password!')
            else:
                messages.error(request, "Email address doesn't exist!")
        return render(request, 'backend/auth/reset_password.html')

class ResetPasswordActivationView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        user_id = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        try:
            user = User.objects.get(user_id=user_id)
            if email_activation_token.check_token(user, token):
                messages.info(request, 'Create a password for your account!')
                return render(request, 'backend/auth/complete_password_reset.html', context)
            else:
                messages.info(request, 'Link broken or Invalid reset link, Please Request a new one!')
                return redirect('auth:reset_password')

        except User.DoesNotExist:
            messages.error(request, 'Oops User not found, hence password cannot be changed, kindly request for a new link!')
            return redirect('auth:reset_password')

    def post(self, request, uidb64, token):
        user_id = force_str(force_bytes(urlsafe_base64_decode(uidb64)).decode())
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user = User.objects.get(user_id=user_id)
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if(password1 != password2):
                messages.error(request, 'Password don\'t match!')
                return render(request, 'backend/auth/complete_password_reset.html', context)

            if(len(password1) < 6):
                messages.error(request, 'Password too short!')
                return render(request, 'backend/auth/complete_password_reset.html', context)

            user.set_password(password1)
            user.save()
            messages.success(request, 'Password Changed you can now login with new password')

            return redirect('auth:login')

        except User.DoesNotExist:
            messages.error(request, 'Snaps user does not exist!')
            return redirect('auth:reset_password')

class TestEmailView(TemplateView):
    template_name = "backend/email/certificate.html"
