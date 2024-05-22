# My django imports
import threading #for enhancing page functionality
from django.core.mail import send_mail #for sending mails
from django.conf import settings #to gain access to variables from the settings
from django.http import request #to gain access to the request object
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import get_template #used for getting html template
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib import messages #for sending messages
from django.conf import settings


# My App imports

class EmailThread(threading.Thread):
    def __init__(self, email_subject, email_body, receiver):
        self.email_subject = email_subject
        self.email_body = email_body
        self.sender = settings.EMAIL_HOST_USER
        self.receiver = receiver
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.email_subject,
            self.email_body,
            self.sender,
            self.receiver,
            html_message=self.email_body,
            fail_silently=False
        )

class AppTokenGenerator(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id)+text_type(timestamp))

email_activation_token = AppTokenGenerator()

class Mailer(View):

    def send(self, user_details, which):
        welcome = 'Welcome to the International Institute of Healthcare Leadership and Quality Improvement!'

        apply_fellowship = 'Acknowledgement of Fellowship Program Application'
        new_fellowship_application = 'A User just applied for the fellowship program'

        apply_webinar = 'Confirmation: Registration for Free Webinar Series'
        new_webinar_application = 'A User just applied for the free webinar series'

        reset = 'Reset Your IIHLM Account Password'
        activate = 'Verify Your IIHLM Email Address'

        if which == 'welcome':
            activation_path = 'backend/email/intro_mail.html'
            receiver = [user_details['email']]
            email_subject = welcome
            context_data = {'name': user_details['name'], 'domain':user_details['domain']}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'apply_fellowship':
            activation_path = 'backend/email/fellowship_mail.html'
            receiver = [user_details['email']]
            email_subject = welcome
            context_data = {'name': user_details['name'], 'domain':user_details['domain']}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'new_fellowship_application':
            activation_path = 'backend/email/applicant_mail.html'
            receiver = [settings.EMAIL_HOST_USER]
            email_subject = new_fellowship_application
            context_data = {
                'name': user_details['name'],
                'domain':user_details['domain'],
                'phone': user_details['phone'],
                'email':user_details['email'],
                'type': "Fellowship Program Applicant",
            }
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'apply_webinar':
            activation_path = 'backend/email/webinar_mail.html'
            receiver = [user_details['email']]
            email_subject = welcome
            context_data = {'name': user_details['name'], 'domain':user_details['domain']}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'new_webinar_application':
            activation_path = 'backend/email/applicant_mail.html'
            receiver = [settings.EMAIL_HOST_USER]
            email_subject = new_fellowship_application
            context_data = {
                'name': user_details['name'],
                'domain':user_details['domain'],
                'phone': user_details['phone'],
                'email':user_details['email'],
                'type': "Free Webinar Series Registration",
            }
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        elif which == 'reset':
            link = reverse('auth:reset_password_activation', kwargs={'uidb64':user_details['uid'], 'token':user_details['token']})
            activation_url = settings.HTTP+user_details['domain']+link
            activation_path = 'backend/email/reset_password.html'
            receiver = [user_details['email']]
            email_subject = reset
            context_data = {'name': user_details['name'], 'reset': activation_url}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()


Email = Mailer()