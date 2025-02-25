from django.urls import path
from loans.views import LoanCreateView, LoanUserView

app_name = 'loans' 

urlpatterns = [
    path('create/', LoanCreateView.as_view(), name='loan_create'),
    path('user_loan/', LoanUserView.as_view(), name='user_loan'),
]