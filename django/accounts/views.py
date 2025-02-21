from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import APIClient

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            response = APIClient.login(username, password)
            print(f"Response from API login: {response}")  # Debug log
            
            if response and 'access_token' in response:
                request.session['token'] = response['access_token']
                user_info = APIClient.get_user_info(response['access_token'])
                print(f"User info from API: {user_info}")  # Debug log
                
                if user_info:
                    request.session['user_info'] = user_info  # Stocke toutes les infos utilisateur
                    request.session['user_role'] = user_info.get('role')  # Stocke spécifiquement le rôle
                    print(f"Role stored in session: {request.session['user_role']}")  # Debug
                    return redirect('accounts:dashboard')
                else:
                    messages.error(request, "Impossible de récupérer les informations utilisateur")
            else:
                messages.error(request, 'Identifiants invalides')
        except Exception as e:
            print(f"Exception during login: {e}")  # Debug log
            messages.error(request, str(e))
    
    return render(request, 'accounts/login.html')


def dashboard_view(request):
    user_info = request.session.get('user_info')
    print(f"User info from session: {user_info}")  # Debug
    
    if not user_info:
        return redirect('accounts:login')
    
    # Comparaison insensible à la casse
    is_advisor = user_info.get('role', '').upper() == 'CONSEILLER'
    print(f"Is advisor: {is_advisor}, Role: {user_info.get('role')}")  # Debug
    
    template = 'accounts/advisor_dashboard.html' if is_advisor else 'accounts/client_dashboard.html'
    print(f"Selected template: {template}")  # Debug
    
    return render(request, template, {'user': user_info})


def logout_view(request):
    request.session.flush()
    return redirect('accounts:login')