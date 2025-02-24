from django.urls import path
from .views import loan_application_by_user
from loans.views import LoanCreateView, LoanUserView

app_name = 'loans' 

urlpatterns = [
    path('create/', LoanCreateView.as_view(), name='loan_create'),
    path('user_loan/', LoanUserView.as_view(), name='user_loan'),
]