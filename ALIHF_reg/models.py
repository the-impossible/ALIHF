from django.db import models
import uuid
from django.shortcuts import reverse

# My app imports
from ALIHF_auth.models import *

# Create your models here.
# Helper Tables
class Gender(models.Model):
    gender_title = models.CharField(max_length=7)

    def __str__(self):
        return self.gender_title

    class Meta:
        db_table = 'Gender'
        verbose_name_plural = 'Gender'

class Countries(models.Model):
    country = models.CharField(max_length=7)

    def __str__(self):
        return self.country

    class Meta:
        db_table = 'Countries'
        verbose_name_plural = 'Countries'

class RelationshipType(models.Model):
    relationship = models.CharField(max_length=7)

    def __str__(self):
        return self.relationship

    class Meta:
        db_table = 'Relationship Type'
        verbose_name_plural = 'Relationship Type'

class GovernmentID(models.Model):
    id_type = models.CharField(max_length=100)

    def __str__(self):
        return self.id_type

    class Meta:
        db_table = 'GovernmentID'
        verbose_name_plural = 'GovernmentID'

class Qualifications(models.Model):
    qualification = models.CharField(max_length=100)

    def __str__(self):
        return self.qualification

    class Meta:
        db_table = 'Qualifications'
        verbose_name_plural = 'Qualifications'

# Main Tables
class ContactInformation(models.Model):

    contact_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    program_id = models.OneToOneField(to="FellowshipProgram", on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_or_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    identification_type = models.ForeignKey(to=GovernmentID, on_delete=models.CASCADE)
    issued_id_number = models.CharField(max_length=100)
    # social_security_number = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.program_id.user_id} has submitted contact / identification information"

    class Meta:
        db_table = 'Contact Information'
        verbose_name_plural = 'Contact Information'

class EducationalBackgroundInformation(models.Model):

    education_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    program_id = models.OneToOneField(to="FellowshipProgram", on_delete=models.CASCADE)
    highest_qualification = models.ForeignKey(to=Qualifications, on_delete=models.CASCADE, related_name="highest_qualification")
    name_of_educational_institution = models.CharField(max_length=100)
    degrees_obtained_and_dates = models.TextField(max_length=500)
    professional_credentials = models.ManyToManyField(Qualifications)
    certifications = models.CharField(max_length=500)
    memberships = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.program_id.user_id.name} has submitted educational background information"

    class Meta:
        db_table = 'Educational Background Information'
        verbose_name_plural = 'Educational Background Information'

class EmploymentHistory(models.Model):

    employment_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    program_id = models.OneToOneField(to="FellowshipProgram", on_delete=models.CASCADE)
    current_employer = models.CharField(max_length=100)
    previous_employer = models.CharField(max_length=100)
    current_job_title = models.CharField(max_length=100)
    current_job_description = models.CharField(max_length=500)
    date_of_employment = models.DateField()
    resume_or_cv = models.FileField(upload_to='uploads/resume/')
    personal_statement = models.TextField(max_length=500)
    letter_of_recommendation = models.FileField(upload_to='uploads/recommendation/')

    def __str__(self):
        return f"{self.program_id.user_id.name} has submitted Employment History"

    class Meta:
        db_table = 'Employment History'
        verbose_name_plural = 'Employment History'

class EmergencyInformation(models.Model):

    emergency_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    program_id = models.OneToOneField(to="FellowshipProgram", on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=100)
    contact_relationship = models.ForeignKey(to=RelationshipType, on_delete=models.CASCADE)
    contact_phone_number = PhoneNumberField(db_index=True, unique=True, blank=True)
    contact_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.program_id.user_id.name} has submitted Employment History"

    class Meta:
        db_table = 'Emergency Information'
        verbose_name_plural = 'Emergency Information'

class BioMedInformation(models.Model):

    bio_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    program_id = models.OneToOneField(to="FellowshipProgram", on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(to=Gender, on_delete=models.CASCADE)
    medical_info = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.program_id.user_id.name} has submitted BioMed Information"

    class Meta:
        db_table = 'BioMed Information'
        verbose_name_plural = 'BioMed Information'

class FellowshipProgram(models.Model):

    fellowship_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.OneToOneField(to=User, on_delete=models.CASCADE, blank=True, null=True)
    contact_information = models.OneToOneField(to=ContactInformation, on_delete=models.CASCADE, blank=True, null=True)
    education_background_information = models.OneToOneField(to=EducationalBackgroundInformation, on_delete=models.CASCADE, blank=True, null=True)
    employment_history = models.OneToOneField(to=EmploymentHistory, on_delete=models.CASCADE, blank=True, null=True)
    emergency_information = models.OneToOneField(to=EmergencyInformation, on_delete=models.CASCADE, blank=True, null=True)
    biodata_and_medical_information = models.OneToOneField(to=BioMedInformation, on_delete=models.CASCADE, blank=True, null=True)
    is_fellowship = models.BooleanField(default=False)
    is_webinar = models.BooleanField(default=False)
    fellowship_approved = models.BooleanField(default=False)
    webinar_approved = models.BooleanField(default=False)
    data_processing_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} has applied for the fellowship program"

    class Meta:
        db_table = 'Fellowship Program'
        verbose_name_plural = 'Fellowship Program'

class WebinarSurveys(models.Model):

    survey_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    survey_title = models.CharField(max_length=100)
    accepting_response = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    link = models.URLField()
    frame_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.survey_title} : {self.link}"

    class Meta:
        db_table = 'Webinar Surveys'
        verbose_name_plural = 'Webinar Surveys'
