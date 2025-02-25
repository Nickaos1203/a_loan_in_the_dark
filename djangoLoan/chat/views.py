from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatMessage
from accounts.models import CustomUser

def chat_room(request):
    # Vérification supplémentaire (optionnelle car le middleware fait déjà cette vérification)
    if not request.session.get('token') or not request.session.get('user_info'):
        return redirect('/accounts/login/?next=' + request.path)
    
    # Récupère les 100 derniers messages
    messages = ChatMessage.objects.all().order_by('-timestamp')[:100]
    messages = reversed(messages)  # Inverser pour afficher les plus anciens d'abord
    
    return render(request, 'chat/chat_room.html', {
        'messages': messages,
        'user_info': request.session.get('user_info'),
        'settings': settings
    })

def message_list(request):
    # Vérification supplémentaire
    if not request.session.get('token') or not request.session.get('user_info'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    messages = ChatMessage.objects.all().order_by('-timestamp')[:100]
    
    # Convertir les messages en liste de dictionnaires
    message_list = []
    for msg in reversed(list(messages)):
        message_list.append({
            'id': msg.id,
            'content': msg.content,
            'user_email': msg.user.email,
            'timestamp': msg.formatted_timestamp,
            'is_staff': msg.is_staff
        })
    
    return JsonResponse({'messages': message_list})

@require_POST
def send_message(request):
    # Vérification supplémentaire
    if not request.session.get('token') or not request.session.get('user_info'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    content = request.POST.get('content')
    if not content:
        return JsonResponse({'error': 'Message content is required'}, status=400)
    
    # Récupérer l'utilisateur actuel
    user_id = request.session.get('user_info', {}).get('id')
    if not user_id:
        return JsonResponse({'error': 'User not found'}, status=401)
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    # Créer le message
    message = ChatMessage.objects.create(
        user=user,
        content=content
    )
    
    # Diffuser le message via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chat_general",
        {
            'type': 'chat_message',
            'message': {
                'id': message.id,
                'content': message.content,
                'user_email': message.user.email,
                'timestamp': message.formatted_timestamp,
                'is_staff': message.is_staff
            }
        }
    )
    
    return JsonResponse({'status': 'success'})
