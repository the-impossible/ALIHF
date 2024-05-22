from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.core.validators import MaxLengthValidator

from ALIHF_reg.models import *

class ContactInformationForm(forms.ModelForm):

    street_address = forms.CharField(help_text='Enter your street address', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    city = forms.CharField(help_text='Enter your city', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    state_or_province = forms.CharField(help_text='Enter your state or province', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    postal_code = forms.CharField(help_text='Enter your postal code', widget=forms.TextInput(
        attrs={
            'class': 'form-control ',
            'type': 'text',
        }
    ))

    country = forms.ModelChoiceField(queryset=Countries.objects.all(), empty_label="(Select country)", help_text='Select country')

    nationality = forms.CharField(help_text='Enter your nationality', widget=forms.TextInput(
        attrs={
            'class': 'form-control ',
            'type': 'text',
        }
    ))

    identification_type = forms.ModelChoiceField(queryset=GovernmentID.objects.all(), empty_label="(Select identification type)", help_text='Select identification type')

    issued_id_number = forms.CharField(help_text='Enter ID number of the identification type selected above', widget=forms.TextInput(
        attrs={
            'class': 'form-control ',
            'type': 'text',
        }
    ))


    class Meta:
        model = ContactInformation
        fields = ('street_address', 'city', 'state_or_province', 'postal_code', 'country', 'nationality', 'identification_type', 'issued_id_number')

class EducationalBackgroundInformationForm(forms.ModelForm):

    highest_qualification = forms.ModelChoiceField(queryset=Qualifications.objects.all(), empty_label="(Select your highest level of qualification)", help_text='Select highest level of qualification')

    name_of_educational_institution = forms.CharField(help_text='Enter the name of your educational institution', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    degrees_obtained_and_dates = forms.CharField(help_text='Enter your degrees obtained with dates', widget=forms.Textarea())

    professional_credentials = forms.ModelMultipleChoiceField(queryset=Qualifications.objects.all(), help_text='Select all your professional credentials')

    certifications = forms.CharField(help_text='Current professional licensure or certifications (if applicable)', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    memberships = forms.CharField(help_text='Professional organization memberships (if applicable)', required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))


    class Meta:
        model = EducationalBackgroundInformation
        fields = ('highest_qualification', 'name_of_educational_institution', 'degrees_obtained_and_dates', 'professional_credentials', 'certifications', 'memberships')

class EmploymentHistoryForm(forms.ModelForm):

    current_employer = forms.CharField(help_text='Enter your current employer', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    previous_employer = forms.CharField(help_text='Enter your previous employer', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    current_job_title = forms.CharField(help_text='Enter your current job title', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    current_job_description = forms.CharField(help_text='Enter your current job description', widget=forms.Textarea())

    date_of_employment = forms.CharField(help_text='Enter the date of employment', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'date',
        }
    ))

    resume_or_cv = forms.FileField(help_text='Upload your resume or cv', widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': '.pdf'
        }
    ))

    personal_statement = forms.CharField(help_text='Enter your personal_statement, maximum 500 characters', widget=forms.Textarea(), validators=[MaxLengthValidator(limit_value=500, message="Not more than 500 characters")])


    letter_of_recommendation = forms.FileField(help_text='Upload your letter of recommendation', widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': '.pdf'
        }
    ))


    class Meta:
        model = EmploymentHistory
        fields = ('current_employer', 'previous_employer', 'current_job_title', 'current_job_description', 'date_of_employment', 'resume_or_cv', 'personal_statement', 'letter_of_recommendation')

class EmergencyInformationForm(forms.ModelForm):

    contact_name = forms.CharField(help_text='Enter your emergency contact name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))

    contact_relationship = forms.ModelChoiceField(queryset=RelationshipType.objects.all(), empty_label="(Select relationship )", help_text='Select relationship type to emergency contact')

    contact_phone_number = PhoneNumberField(help_text='Enter emergency contact phone number')

    contact_address = forms.CharField(help_text='Enter your emergency contact address', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
        }
    ))


    class Meta:
        model = EmergencyInformation
        fields = ('contact_name', 'contact_relationship', 'contact_phone_number', 'contact_address')

class BioMedInformationForm(forms.ModelForm):

    date_of_birth = forms.CharField(help_text='Enter your date of birth', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'date',
        }
    ))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="(Select gender )", help_text='Select your gender')

    medical_info = forms.CharField(help_text='Enter any relevant medical conditions or disabilities that may require accommodation during the fellowship program', widget=forms.Textarea(), validators=[MaxLengthValidator(limit_value=500, message="Not more than 500 characters")])

    class Meta:
        model = BioMedInformation
        fields = ('date_of_birth', 'gender', 'medical_info')

class FellowshipProgramForm(forms.ModelForm):

    class Meta:
        model = FellowshipProgram
        fields = ('contact_information', 'education_background_information', 'employment_history', 'emergency_information', 'biodata_and_medical_information', 'data_processing_consent')


