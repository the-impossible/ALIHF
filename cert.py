# My django imports
import threading #for enhancing page functionality
from django.core.mail import EmailMessage #for sending mails
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
import cv2
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ALIHF_project.settings")
django.setup()

class EmailThread(threading.Thread):
    def __init__(self, email_subject, email_body, receiver, attachment=None):
        self.email_subject = email_subject
        self.email_body = email_body
        self.sender = settings.EMAIL_HOST_USER
        self.receiver = receiver
        self.attachment = attachment
        threading.Thread.__init__(self)

    def run(self):

        email = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.sender,
            to=self.receiver,
        )

        email.content_subtype = "html"  # Set the email content type to HTML

        if self.attachment:
            email.attach_file(self.attachment)
        email.send(fail_silently=False)


class Mailer(View):

    def send(self, user_details):
        subject = 'Your Certificate of Participation on our Webinar Series'

        activation_path = 'backend/email/certificate.html'
        receiver = [user_details['email']]
        email_subject = subject
        context_data = {'name': user_details['name'],}
        attachment_path = user_details['attachment_path']
        email_body = get_template(activation_path).render(context_data)
        EmailThread(email_subject, email_body, receiver, attachment_path).start()

Email = Mailer()

list_name = [
    ['Dr. Adesola Oyinide', 'vastoutlet.ecommerce@gmail.com'],
    ['Richard Emmanuel Eghenayarhiore', 'richardemmanuel45@gmail.com'],
]

for index, details in enumerate(list_name):

    template = cv2.imread(rf'certificate.jpg')

    cv2.putText(template, details[0], (270, 375), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)
    cert_name = f"{details[0].split(' ')[1]}.jpg"
    cv2.imwrite(rf"generated_cert\{cert_name}", template)

    user_details = {
        'email': details[1],
        'name': details[0],
        'attachment_path': f"generated_cert\{cert_name}"
    }

    Email.send(user_details=user_details)

    print(f"Processing Certificate {index + 1}/{len(list_name)}")
