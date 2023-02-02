from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import serializers


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
    redirect = request.GET['next']
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(request.POST[redirect])
        else:
            return render(request, 'chat/login.html', {'error': 'Invalid Login Credentials',
                                                       'wrong_password': True,
                                                       'redirect': redirect})
    return render(request, 'chat/login.html', {'redirect': redirect})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
            )
            login(request, user)
            return redirect('/chat/')
    else:
        return render(request, 'chat/signUp.html')


def logout(request):
    pass
