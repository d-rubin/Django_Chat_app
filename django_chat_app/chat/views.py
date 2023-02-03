from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def chat_view(request):
    """
    This is a view to render the chat.
    :param request: The request method (POST or GET)
    :return: The chat.html or the new message
    """
    if request.method == 'POST':
        my_chat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['text'],
                                             chat=my_chat, author=request.user,
                                             receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message])
        return JsonResponse(serialized_obj[1: -1], safe=False)
    chat_messages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/chat.html', {'messages': chat_messages})


def login_view(request):
    redirect_to = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_to)
        else:
            return render(request, 'chat/login.html', {
                'error': 'Invalid Login Credentials',
                'wrong_password': True,
                'redirect': redirect_to
            })
    return render(request, 'chat/login.html', {'redirect': redirect_to})


def register_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )
        user.save()
        login(request, user)
        return redirect('/chat/')
    else:
        return render(request, 'chat/signUp.html')


def logout_view(request):
    logout(request)
