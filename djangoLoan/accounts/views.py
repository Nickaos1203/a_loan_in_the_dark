from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from .utils import APIClient
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from accounts.forms import UserCreateForm
from django.conf import settings
import os 
import requests
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        email = form.cleaned_data.get('username')  # Récupère l'email
        password = form.cleaned_data.get('password')  # Récupère le mot de passe
        
        try:
            # Essaye de te connecter via l'API
            response = APIClient.login(email, password)
            if response and 'access_token' in response:
                token = response['access_token']
                self.request.session['token'] = token
                user_info = APIClient.get_user_info(response['access_token'])
                User = get_user_model()
                current_user, created = User.objects.get_or_create(id=user_info['id'])

                # Met à jour le modèle utilisateur avec le token API
                current_user.api_token = token
                current_user.save()

                # Connecte l'utilisateur à Django
                login(self.request, current_user) 

                # Sauvegarde des informations utilisateur dans la session
                self.request.session['user_info'] = user_info
                self.request.session['user_is_staff'] = user_info.get('is_staff')

                return redirect('accounts:dashboard')
            else:
                messages.error(self.request, 'Identifiants invalides')
        except Exception as e:
            messages.error(self.request, f"Erreur: {e}")
        
        return HttpResponseRedirect(self.get_redirect_url())

    def get_redirect_url(self):
        return reverse_lazy('accounts:dashboard')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             response = APIClient.login(email, password)
#             print(f"Response from API login: {response}")  # Debug log
            
#             if response and 'access_token' in response:
#                 token = response['access_token']
#                 request.session['token'] = token
#                 user_info = APIClient.get_user_info(response['access_token'])
#                 current_user = get_object_or_404(CustomUser, id=user_info['id'])
#                 print(f"Le gros truc :{current_user}")
#                 current_user.api_token = token
#                 current_user.save()
#                 print(f"User info from API: {user_info}")  # Debug log
                
#                 if user_info:
#                     request.session['user_info'] = user_info  # Stocke toutes les infos utilisateur
#                     request.session['user_is_staff'] = user_info.get('is_staff')  # Stocke spécifiquement le rôle
#                     return redirect('accounts:dashboard')
#                 else:
#                     messages.error(request, "Impossible de récupérer les informations utilisateur")
#             else:
#                 messages.error(request, 'Identifiants invalides')
#         except Exception as e:
#             print(f"Exception during login: {e}")  # Debug log
#             messages.error(request, str(e))
    
#     return render(request, 'accounts/login.html')


# def dashboard_view(request):
#     user_info = request.session.get('user_info')
#     print(f"User info from session: {user_info}")  # Debug
    
#     if not user_info:
#         return redirect('accounts:login')
    
#     # Comparaison insensible à la casse
#     is_advisor = user_info.get('is_staff')
    
#     template = 'accounts/advisor_dashboard.html' if is_advisor else 'accounts/client_dashboard.html'
#     print(f"Selected template: {template}")  # Debug
    
#     return render(request, template, {'user': user_info})

class CreateUserView(CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = "accounts/advisor_dashboard.html"
    success_url = reverse_lazy('accounts:login')
    

    def form_valid(self, form):
        user_info = self.request.session.get('user_info')
        user = get_object_or_404(CustomUser, id=user_info['id'])
        token = user.api_token
        headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
        api_url = os.getenv("API_BASE_URL", settings.API_BASE_URL) + "/create_user"
        django_data = form.cleaned_data
        try:
            response = requests.post(api_url, json=django_data, headers=headers)
            django_data.pop('password', None)
            data = response.json()
            if response.status_code == 201:
                form.instance.id = data.get("id")
                form.instance.password = None
                return super().form_valid(form)
            else:
                return JsonResponse({"error": data}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')