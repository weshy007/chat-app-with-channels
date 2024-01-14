from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Room, Message

# Create your views here.
def index(request):
    room = Room.objects.all()
    
    return render(request, 'index.html', {'room': room})


def room(request, room_name):
    """create room or retrieve it"""
    chat_room, created =  Room.objects.get(name=room_name)
    
    return render(request, 'room.html', {'room': chat_room})


@login_required
def group(request, group_name):
    group = Room.objects.get(id=group_name)
    messages = group.message_set.all()

    context = {
        "messages": messages, 
        "room_name": group_name,
        "name": group
    }

    return render(request, 'group-chat.html', context)


def notice(request):
    return render(request, "base.html")


def talk(request):
    messages = Message.objects.all()
    groups = Room.objects.all()

    context = {
        'messages': messages, 
        'groups': groups}
    
    return render(request, 'talk.html', context)


class RegistrationView(CreateView):
    template_name = 'signup.html'
    model = get_user_model()
    success_url = reverse_lazy("login")


class SigninView(LoginView):
    next_page = '/chat/talk/'
    template_name = 'signin.html'