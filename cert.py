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
from datetime import datetime
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
    ['Dr. Lucky oteheri Omowhara', 'omowharaluckyoteheri87@gmail.com'],
    ['Dr. Lucky oteheri Omowhara', 'doctorlukenzorsanchez@gmail.com'],
    ['Femi Michael Aderibigbe', 'michaelfemi80@gmail.com'],
    ['Dr Adesola A. Oniyide', 'adesolaoniyide@abuad.edu.ng'],
    ['Bunmilola Oyeleye', 'bumbells2003@yahoo.com'],
    ['Dennis Anthony Musango', 'makwallahealthcare@gmail.com'],
    ['Richard Emmanuel Eghenayahiore', 'richardemmanuel45@gmail.com'],
    ['Dr. Joshua Kolawole', 'oshuasj@gmail.com'],
]

for index, details in enumerate(list_name):

    template = cv2.imread(rf'certificate.jpg')

    # Text and font settings
    text = details[0]
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 0.7
    font_thickness = 1

    # Date
    current_date = datetime.now().date()

    # Format the date to day-month-year
    formatted_date = current_date.strftime("%d-%m-%Y")


    # Calculate the text size
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    # Calculate the x-coordinate to center the text
    x_start = 127
    x_end = 599
    y = 309

    x = x_start + (x_end - x_start - text_size[0]) // 2

    cv2.putText(template, text, (x, y), font, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
    cv2.putText(template, str(formatted_date), (210, 517), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), font_thickness, cv2.LINE_AA)

    cert_name = f"{details[0].split(' ')[1]}.jpg"
    cv2.imwrite(rf"generated_cert\{cert_name}", template)

    user_details = {
        'email': details[1],
        'name': details[0],
        'attachment_path': f"generated_cert\{cert_name}"
    }

    Email.send(user_details=user_details)

    print(f"Processing Certificate {index + 1}/{len(list_name)}")
