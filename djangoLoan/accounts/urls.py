from django.urls import path
from . import views
from accounts.views import CreateUserView, RedirectDashboardView, CustomLoginView, FirstLoginView, CustomLogoutView

app_name = 'accounts' 

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('first_login/', FirstLoginView.as_view(), name='first_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', RedirectDashboardView.as_view(), name='dashboard'),
    path('advisor/dashboard/', CreateUserView.as_view(), name='advisor_dashboard'),
    path('user/dashboard/', CreateUserView.as_view(), name='user_dashboard'),
]

#     path('dashboard/', views.dashboard_view, name='user_dashboard'),