class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des URLs qui ne nécessitent pas d'authentification
        public_paths = ['/accounts/login/', '/accounts/logout/']
        
        # Si l'utilisateur est sur une page publique, ne rien faire de spécial
        if request.path in public_paths:
            return self.get_response(request)
        
        # Pour les pages protégées, vérifier l'authentification
        token = request.session.get('token')
        user_info = request.session.get('user_info')

        # Si l'utilisateur n'a pas de token et tente d'accéder à une page protégée
        if not token:
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.warning(request, "Vous devez être connecté.")
            return redirect('accounts:login')

        return self.get_response(request)









# class CustomAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Ne pas appliquer le middleware aux pages de connexion et déconnexion
#         if request.path == '/accounts/login/' or request.path == '/accounts/logout/':
#             return self.get_response(request)
        
#         # Pour les autres pages, simuler un utilisateur authentifié si nécessaire
#         if not request.user.is_authenticated:
#             from django.contrib.auth import get_user_model, login
            
#             User = get_user_model()
#             try:
#                 user = User.objects.get(email="leo@staff.fr")
#                 # Connecter l'utilisateur à Django
#                 login(request, user)
                
#                 # Stocker les informations dans la session
#                 request.session["token"] = "debug_token"
#                 request.session["user_info"] = {
#                     "id": str(user.id),
#                     "email": user.email,
#                     "is_staff": user.is_staff,
#                     "first_connection": False
#                 }
#             except Exception as e:
#                 print(f"Erreur dans le middleware: {e}")
        
#         return self.get_response(request)