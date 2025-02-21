from django.shortcuts import redirect
from django.urls import reverse

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des URLs qui ne nécessitent pas d'authentification
        public_paths = [reverse('accounts:login')]
        
        # Si l'utilisateur n'est pas connecté et essaie d'accéder à une page protégée
        if request.path not in public_paths and not request.session.get('token'):
            return redirect('accounts:login')
            
        response = self.get_response(request)
        return response