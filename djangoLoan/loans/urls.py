from django.urls import path
from .views import loan_application_by_user

urlpatterns = [
    path('form', loan_application_by_user, name='loan_form'),
]