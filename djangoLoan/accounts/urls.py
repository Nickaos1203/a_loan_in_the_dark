from django.urls import path
from . import views
from accounts.views import CreateUserView

app_name = 'accounts' 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Vue du tableau de bord principal
    path('dashboard/create_user/', views.create_user_view, name='create_user'),
]
#ouioui