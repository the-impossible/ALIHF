from django.urls import path
from ALIHF_reg.views import *

app_name = "reg"

urlpatterns = [
    path('apply/<str:type_id>/', ApplyFellowshipPageView.as_view(), name='apply_fellowship'),

    path('submit_contact/<str:type_id>/', SubmitContactInformationView.as_view(), name='submit_contact'),
    path('submit_education/<str:type_id>/', SubmitEducationInformationView.as_view(), name='submit_education'),
    path('submit_employment/<str:type_id>/', SubmitEmploymentInformationView.as_view(), name='submit_employment'),
    path('submit_emergency/<str:type_id>/', SubmitEmergencyInformationView.as_view(), name='submit_emergency'),
    path('submit_bio_med/<str:type_id>/', SubmitBioMedInformationView.as_view(), name='submit_bio_med'),
    path('webinar_survey', WebinarSurvey.as_view(), name='webinar_survey'),
    path('webinar_survey_details/<str:pk>', WebinarSurveyDetailView.as_view(), name='webinar_survey_details'),
]
