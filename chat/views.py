from django.shortcuts import render


def lobby(request):
    return render(request, "chat/chat-base.html")
