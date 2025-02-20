from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class APIAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs qui ne nécessitent pas d'authentification
        public_urls = ['/login/', '/admin/']
        
        # Vérifier si l'URL actuelle nécessite une authentification
        if not any(request.path.startswith(url) for url in public_urls):
            # Vérifier si un token est présent en session
            if not request.session.get('token'):
                messages.warning(request, 'Veuillez vous connecter')
                return redirect('login')
        
        response = self.get_response(request)
        return response