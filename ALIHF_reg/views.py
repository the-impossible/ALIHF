from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
from ALIHF_reg.models import *
from ALIHF_reg.forms import *
from ALIHF_reg.decorators import *
from ALIHF_auth.utils import *

@method_decorator(has_updated, name="get")
class ApplyFellowshipPageView(LoginRequiredMixin, View):
    template_name = "backend/apply/apply_fellowship.html"

    def get_context_data(self, **kwargs):
        user_id = self.request.user.user_id
        type_id = self.kwargs['type_id']

        data = {
            'contact': None,
            'education': None,
            'employment': None,
            'emergency': None,
            'bio': None,
            'consent': False,
            'type': None,
        }

        if type_id == 'fellowship':
            data['type'] = "Fellowship program"
            data['type_url'] = "fellowship"

        elif type_id == 'webinar':
            data['type'] = "Free Webinar Series"
            data['type_url'] = "webinar"

        try:
            fellowship_data = FellowshipProgram.objects.get(user_id=user_id)

            data['record'] = fellowship_data

            if fellowship_data.contact_information != None:
                data['contact'] = 'contact'
            if fellowship_data.education_background_information != None:
                data['education'] = 'education'
            if fellowship_data.employment_history != None:
                data['employment'] = 'employment'
            if fellowship_data.emergency_information != None:
                data['emergency'] = 'emergency'
            if fellowship_data.biodata_and_medical_information != None:
                data['bio'] = 'bio'
            if fellowship_data.data_processing_consent != False:
                data['consent'] = 'consent'

        except FellowshipProgram.DoesNotExist:
            pass
        return data

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        data_processing_consent = request.POST['data_processing_consent']
        type_id = self.kwargs['type_id']

        if data_processing_consent:

            application = FellowshipProgram.objects.filter(user_id=self.request.user).first()

            if application and application.contact_information and application.education_background_information and application.employment_history and application.emergency_information and application.biodata_and_medical_information:
                application.data_processing_consent = True

                if type_id == 'fellowship':
                    application.is_fellowship = True

                elif type_id == 'webinar':
                    application.is_webinar = True

                application.save()

                messages.success(request, "Application successful, we will reach out shortly")

                # SEND EMAIL
                user_details = {
                    'name':application.user_id.name,
                    'email': application.user_id.email,
                    'phone': application.user_id.phone_number,
                    'domain': get_current_site(self.request).domain,
                }

                if type_id == 'fellowship':
                    Email.send(user_details, 'apply_fellowship')
                    Email.send(user_details, 'new_fellowship_application')

                elif type_id == 'webinar':
                    Email.send(user_details, 'apply_webinar')
                    Email.send(user_details, 'new_webinar_application')

            else:
                messages.error(request, "Fill out the necessary forms!")

        else:
            messages.error(request, "You have to consent to data processing")
        return render(request, self.template_name, self.get_context_data())

class SubmitContactInformationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactInformation
    form_class = ContactInformationForm
    template_name = "backend/apply/submit_info.html"
    success_message = "Contact information submitted, proceed with education information"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Contact Information"
        return context

    def dispatch(self, request, *args, **kwargs):
        previous_record = FellowshipProgram.objects.filter(user_id=self.request.user).first()
        if previous_record and previous_record.contact_information:
            messages.warning(request, "Entries already exist")
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # create a new fellowship program
        fellowship, created = FellowshipProgram.objects.get_or_create(user_id=self.request.user)

        # Save the contact information
        contact_form = form.save(commit=False)
        contact_form.program_id = fellowship
        contact_form.save()

        # Assign the ContactInformation ID to the FellowshipProgram instance
        fellowship.contact_information = contact_form
        fellowship.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        type_id = self.kwargs['type_id']
        messages.success(self.request, self.success_message)

        return reverse("reg:apply_fellowship", kwargs={'type_id': type_id})

class SubmitEducationInformationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EducationalBackgroundInformation
    form_class = EducationalBackgroundInformationForm
    template_name = "backend/apply/submit_info.html"
    success_message = "Education information submitted, proceed with employment history information"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Education Background Information"
        return context

    def dispatch(self, request, *args, **kwargs):
        previous_record = FellowshipProgram.objects.filter(user_id=self.request.user).first()

        if previous_record and previous_record.education_background_information:
            messages.warning(request, "Entries already exist")
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # create a new fellowship program
        fellowship, created = FellowshipProgram.objects.get_or_create(user_id=self.request.user)

        # Save the contact information
        contact_form = form.save(commit=False)
        contact_form.program_id = fellowship
        contact_form.save()

        # Assign the ContactInformation ID to the FellowshipProgram instance
        fellowship.education_background_information = contact_form
        fellowship.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        type_id = self.kwargs['type_id']
        messages.success(self.request, self.success_message)
        return reverse("reg:apply_fellowship", kwargs={'type_id': type_id})

class SubmitEmploymentInformationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EmploymentHistory
    form_class = EmploymentHistoryForm
    template_name = "backend/apply/submit_info.html"
    success_message = "Employment history information submitted, proceed with emergency information"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Employment history Information"
        return context

    def dispatch(self, request, *args, **kwargs):
        previous_record = FellowshipProgram.objects.filter(user_id=self.request.user).first()

        if previous_record and previous_record.employment_history:
            messages.warning(request, "Entries already exist")
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # create a new fellowship program
        fellowship, created = FellowshipProgram.objects.get_or_create(user_id=self.request.user)

        # Save the contact information
        employment_form = form.save(commit=False)
        employment_form.program_id = fellowship
        employment_form.save()

        # Assign the employment_history ID to the FellowshipProgram instance
        fellowship.employment_history = employment_form
        fellowship.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        type_id = self.kwargs['type_id']
        messages.success(self.request, self.success_message)
        return reverse("reg:apply_fellowship", kwargs={'type_id': type_id})

class SubmitEmergencyInformationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = EmergencyInformation
    form_class = EmergencyInformationForm
    template_name = "backend/apply/submit_info.html"
    success_message = "Emergency information submitted, proceed with Bio-Medical information"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Emergency Information"
        return context

    def dispatch(self, request, *args, **kwargs):
        previous_record = FellowshipProgram.objects.filter(user_id=self.request.user).first()

        if previous_record and previous_record.emergency_information:
            messages.warning(request, "Entries already exist")
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # create a new fellowship program
        fellowship, created = FellowshipProgram.objects.get_or_create(user_id=self.request.user)

        # Save the contact information
        emergency_form = form.save(commit=False)
        emergency_form.program_id = fellowship
        emergency_form.save()

        # Assign the employment_history ID to the FellowshipProgram instance
        fellowship.emergency_information = emergency_form
        fellowship.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        type_id = self.kwargs['type_id']
        messages.success(self.request, self.success_message)
        return reverse("reg:apply_fellowship", kwargs={'type_id': type_id})

class SubmitBioMedInformationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BioMedInformation
    form_class = BioMedInformationForm
    template_name = "backend/apply/submit_info.html"
    success_message = "Bio Medical Information has been  submitted, proceed with consenting to data processing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Bio-Medical Information"
        return context

    def dispatch(self, request, *args, **kwargs):

        previous_record = FellowshipProgram.objects.filter(user_id=self.request.user).first()

        if previous_record and previous_record.biodata_and_medical_information:
            messages.warning(request, "Entries already exist")
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # create a new fellowship program
        fellowship, created = FellowshipProgram.objects.get_or_create(user_id=self.request.user)

        # Save the contact information
        bio_med_form = form.save(commit=False)
        bio_med_form.program_id = fellowship
        bio_med_form.save()

        # Assign the employment_history ID to the FellowshipProgram instance
        fellowship.biodata_and_medical_information = bio_med_form
        fellowship.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        type_id = self.kwargs['type_id']
        messages.success(self.request, self.success_message)
        return reverse("reg:apply_fellowship", kwargs={'type_id': type_id})

