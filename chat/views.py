from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', {})

@login_required(login_url = 'login')
def room(request, room_name):
    return render(request, 'chat/chatroom.html', {
        'room_name': room_name
    })

@login_required(login_url = 'login')
def enter_room(request):
    return render(request, 'chat/enter_room.html')
