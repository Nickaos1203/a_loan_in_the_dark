from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import APIClient

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Test de connexion
            response = APIClient.login(username, password)
            print(f"Login response: {response}")

            if response and 'access_token' in response:
                token = response['access_token']
                request.session['token'] = token
                
                # Test de récupération des infos utilisateur
                user_info = APIClient.get_user_info(token)
                print(f"User info: {user_info}")
                
                if user_info:
                    request.session['user_role'] = user_info.get('role')
                    return redirect('dashboard')
                else:
                    messages.error(request, "Impossible de récupérer les informations utilisateur")
            else:
                messages.error(request, 'Identifiants invalides')
        except Exception as e:
            print(f"Exception in login_view: {str(e)}")
            messages.error(request, f'Erreur lors de la connexion: {str(e)}')
    
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    try:
        token = request.session.get('token')
        if not token:
            messages.error(request, "Session expirée")
            return redirect('login')
            
        user_info = APIClient.get_user_info(token)
        if not user_info:
            messages.error(request, "Impossible de récupérer les informations utilisateur")
            return redirect('login')
            
        template = 'accounts/advisor_dashboard.html' if user_info.get('role') == 'CONSEILLER' else 'accounts/client_dashboard.html'
        return render(request, template, {'user': user_info})
    except Exception as e:
        print(f"Exception in dashboard_view: {str(e)}")
        messages.error(request, f"Erreur lors du chargement du dashboard: {str(e)}")
        return redirect('login')