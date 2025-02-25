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
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    logger.debug("Entering login view")
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            logger.debug(f"Login attempt for email: {email}")
            
            response = APIClient.login(email, password)
            
            if response and 'access_token' in response:
                token = response['access_token']
                request.session['token'] = token
                
                user_info = APIClient.get_user_info(token)
                if user_info:
                    request.session['user_info'] = user_info
                    request.session['user_is_staff'] = user_info.get('is_staff')
                    return redirect('accounts:dashboard')
                else:
                    messages.error(request, "Impossible de récupérer les informations utilisateur")
            else:
                messages.error(request, 'Identifiants invalides')
        
        logger.debug("Rendering login template")
        return render(request, 'accounts/login.html')
    
    except Exception as e:
        logger.exception("Error in login view")
        messages.error(request, f"Une erreur s'est produite: {str(e)}")
        return render(request, 'accounts/login.html')

def dashboard_view(request):
    user_info = request.session.get('user_info')
    
    if not user_info:
        return redirect('accounts:login')
    
    is_advisor = user_info.get('is_staff', False)
    template = 'accounts/advisor_dashboard.html' if is_advisor else 'accounts/client_dashboard.html'
    
    return render(request, template, {'user': user_info})
class CreateUserView(CreateView):
    model = CustomUser
    form_class = UserCreate
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
        print(f"password :{django_data}")
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

def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')