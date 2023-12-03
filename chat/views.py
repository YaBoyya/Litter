from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import ChatRoom
from users.models import LitterUser


def lobby(request):
    rooms = ChatRoom.objects.filter(users=request.user)
    q = request.session.pop('q', request.GET.get('q', ''))
    search_rooms = ChatRoom.objects.filter(is_private=False, title__contains=q)
    context = {'rooms': rooms, 'search_rooms': search_rooms, 'q': q}
    return render(request, "chat/chat-base.html",  context)


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
    return redirect('chat:room', room.uuid)


def group_join(request, uuid):
    room = ChatRoom.objects.get(uuid=uuid)
    if request.user in room.users.all():
        room.users.remove(request.user)
    else:
        room.users.add(request.user)
    return redirect('chat:room', uuid)


def chat_room(request, uuid):
    if request.GET.get('q'):
        request.session['q'] = request.GET.get('q')
        return redirect('chat:lobby')
    rooms = ChatRoom.objects.filter(users=request.user)
    room = get_object_or_404(ChatRoom, uuid=uuid)
    messages = room.messages.all()
    context = {'rooms': rooms, 'room': room,
               'messages': messages}
    return render(request, 'chat/conversation.html', context)