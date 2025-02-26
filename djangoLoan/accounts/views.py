from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .utils import APIClient
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, View
from accounts.forms import UserCreate
from django.conf import settings
import os 
import requests
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView

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
                current_user, is_create = User.objects.get_or_create(id=user_info['id'])
                print(current_user)

                # Met à jour le modèle utilisateur avec le token API
                current_user.api_token = token
                current_user.save()
                login(self.request, current_user) 
                print(f"utilisateur authentifié : {self.request.user}")

                # Sauvegarde des informations utilisateur dans la session
                self.request.session['user_info'] = user_info
                self.request.session['user_is_staff'] = user_info.get('is_staff')

                return redirect('accounts:dashboard')
            else:
                messages.error(self.request, 'Identifiants invalides')
        except Exception as e:
            messages.error(self.request, f"Erreur: {e}")
        
        return redirect('accounts:dashboard')
    
    def get_redirect_url(self):
        redirect('accounts:dashboard')


class RedirectDashboardView(View):
    def get(self, request, *args, **kwargs):
        print(f"request user :{self.request.user}")
        print(f"request session : {self.request.session['user_info']}")
        if request.user.is_staff:
            return redirect('accounts:advisor_dashboard')
        else:
            return redirect('accounts:user_dashboard')


class CreateUserView(CreateView):
    model = CustomUser
    form_class = UserCreate
    template_name = "accounts/advisor_dashboard.html"
    success_url = reverse_lazy('accounts:advisor_dashboard')
    

    def form_valid(self, form):
        # print(f"request user :{self.request.user}")
        # print(f"request session : {self.request.session['user_info']}")
        # user_info = self.request.session.get('user_info')
        # print(f"user info : {user_info}")
        token = self.request.user.api_token
        headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
        api_url = os.getenv("API_BASE_URL", settings.API_BASE_URL) + "/create_user"
        django_data = form.cleaned_data
        django_data["password"] = "password1234"
        try:
            response = requests.post(api_url, json=django_data, headers=headers)
            data = response.json()
            if response.status_code == 201:
                form.instance.id = data.get("id")
                return super().form_valid(form)
            else:
                return JsonResponse({"error": data}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def get_redirect_url(self):
        redirect('accounts:dashboard')

def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')