from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .utils import APIClient
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from accounts.forms import UserCreate
from django.conf import settings
import os 
import requests
from django.http import JsonResponse
from django.urls import reverse_lazy


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            response = APIClient.login(email, password)
            print(f"Response from API login: {response}")  # Debug log
            
            if response and 'access_token' in response:
                token = response['access_token']
                request.session['token'] = token
                user_info = APIClient.get_user_info(response['access_token'])
                current_user = get_object_or_404(CustomUser, id=user_info['id'])
                print(f"Le gros truc :{current_user}")
                current_user.api_token = token
                current_user.save()
                print(f"User info from API: {user_info}")  # Debug log
                
                if user_info:
                    request.session['user_info'] = user_info  # Stocke toutes les infos utilisateur
                    request.session['user_is_staff'] = user_info.get('is_staff')  # Stocke spécifiquement le rôle
                    return redirect('accounts:dashboard')
                else:
                    messages.error(request, "Impossible de récupérer les informations utilisateur")
            else:
                messages.error(request, 'Identifiants invalides')
        except Exception as e:
            print(f"Exception during login: {e}")  # Debug log
            messages.error(request, str(e))
    
    return render(request, 'accounts/login.html', {'settings': settings})

class CreateUserView(CreateView):
    model = CustomUser
    form_class = UserCreate
    template_name = "accounts/advisor_dashboard.html"
    success_url = reverse_lazy('accounts:dashboard')  # Changé de login à dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = settings
        
        # Ajout de la liste des utilisateurs pour l'affichage
        if self.request.session.get('token'):
            user_info = self.request.session.get('user_info')
            if user_info and user_info.get('is_staff'):
                api_url = f"{settings.API_BASE_URL}/list"
                headers = {
                    "Authorization": f"Bearer {self.request.session['token']}",
                    "Accept": "application/json"
                }
                try:
                    response = requests.get(api_url, headers=headers)
                    if response.ok:
                        context['users'] = response.json()
                except:
                    context['users'] = []
        
        return context

    def form_valid(self, form):


        user_info = self.request.session.get('user_info')
        token = self.request.session.get('token')
        
        if not token or not user_info:
            return JsonResponse({"error": "Non autorisé"}, status=401)

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        data = {
            "email": form.cleaned_data['email'],
            "password": form.cleaned_data['password'],
            "is_staff": form.cleaned_data['is_staff']
        }

        api_url = f"{settings.API_BASE_URL}/create_user"
        
        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.ok:
                form.instance.id=response.json().get("id")
                messages.success(self.request, "Utilisateur créé avec succès")
                return super().form_valid(form)
            else:
                messages.error(self.request, f"Erreur: {response.json().get('detail', 'Erreur inconnue')}")
                return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Erreur: {str(e)}")
            return self.form_invalid(form)

def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')

def dashboard_view(request):
    token = request.session.get('token')
    user_info = request.session.get('user_info')
    
    print(f"Token dans session: {token is not None}")
    
    if not token or not user_info:
        return redirect('accounts:login')
    
    is_advisor = user_info.get('is_staff', False)
    template = 'accounts/advisor_dashboard.html' if is_advisor else 'accounts/client_dashboard.html'
    
    return render(request, template, {
        'user': user_info,
        'settings': settings
    })