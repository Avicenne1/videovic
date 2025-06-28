from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def room(request, room_name):
    return render(request, 'chatvideo/room.html', {
        'room_name': room_name,
        'username': request.user.username,
        'section': 'people'
    })

@login_required
def lobby(request):
    return render(request, 'chatvideo/lobby.html', {'section': 'people'})
