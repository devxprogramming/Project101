from django.shortcuts import render, redirect, get_object_or_404
from classroom.forms import RoomForm
from classroom.models import Room

def create_room(request):
    page = 'create_room'
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('dashboard')
        else:
            form = RoomForm()
        
    context = {
        'page':page,
        'form': form,
    }
    return render(request, 'room/create_update.html', context)


def update_room(request, pk):
    page = 'update_room'
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
    context = {
        'page':page,
        'form':form,
    }
        
    return render(request, 'room/create_update.html', context)