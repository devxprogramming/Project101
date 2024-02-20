from django.shortcuts import render, redirect, get_object_or_404
from classroom.forms import RoomForm
from classroom.models import Room

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('dashboard')
    return render(request, 'room/create_room.hmtl')