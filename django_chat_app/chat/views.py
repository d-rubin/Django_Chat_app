from django.shortcuts import render
from .models import Chat, Message


def index(request):
    if request.method == 'POST':
        my_chat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['text'],
                               chat=my_chat, author=request.user,
                               receiver=request.user)
    chat_messages = Message.objects.filter(chat__id=1)

    return render(request, 'chat/index.html', {'username': request.user.first_name, 'messages': chat_messages})
