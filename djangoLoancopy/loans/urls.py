from django.urls import path
from loans.views import LoanCreateView

app_name = 'loans' 

urlpatterns = [
    path('create/', LoanCreateView.as_view, name='loan_create'),
]