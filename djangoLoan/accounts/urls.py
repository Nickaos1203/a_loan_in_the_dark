from django.urls import path
from . import views
from accounts.views import CreateUserView, CustomLoginView, RedirectDashboardView

app_name = 'accounts' 

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', RedirectDashboardView.as_view(), name='dashboard'),
    path('advisor/dashboard/', CreateUserView.as_view(), name='advisor_dashboard'),
    path('advisor/dashboard/', CreateUserView.as_view(), name='advisor_dashboard'),
]

#     path('dashboard/', views.dashboard_view, name='user_dashboard'),