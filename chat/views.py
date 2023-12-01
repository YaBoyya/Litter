from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import ChatRoom
from users.models import LitterUser


def lobby(request):
    return render(request, "chat/chat-base.html")


def chat_redirect(request, pk):
    user = get_object_or_404(LitterUser, id=pk)
    try:
        room = ChatRoom.objects.filter(
            users__in=[user, request.user]
            ).annotate(users_num=Count('users')).get(users_num=2)
    except ChatRoom.DoesNotExist:
        room = ChatRoom.objects.create()
        room.users.add(request.user, user)
    print(room)
    return redirect('chat:room', room.id)


def chat_room(request, pk):
    room = get_object_or_404(ChatRoom, id=pk)
    messages = room.messages.all()
    context = {'room': room, 'messages': messages, 'pk': pk}
    return render(request, 'chat/conversation.html', context)
