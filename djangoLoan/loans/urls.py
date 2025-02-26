from django.urls import path
from loans.views import LoanCreateView, LoanUserView, AdvisorLoanDetailView

app_name = 'loans' 

urlpatterns = [
    path('create/', LoanCreateView.as_view(), name='loan_create'),
    path('user_loan/', LoanUserView.as_view(), name='user_loan'),
    path('advisor/loan/<uuid:pk>/', AdvisorLoanDetailView.as_view(), name='advisor_loan'),
    path('advisor/loan/<uuid:pk>/update/', AdvisorLoanDetailView.as_view(), name='update'),
]