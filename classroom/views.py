from django.shortcuts import render, redirect, get_object_or_404
from classroom.forms import RoomForm
from classroom.models import Room
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def create_room(request):
    if request.user.profile.account_type == 'Student':
        return redirect('dashboard')
    page = 'create_room'
    form = RoomForm
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('all_rooms')
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


def delete_room(request, pk):
    room = Room.objects.get(room_code=pk)
    if request.method == "POST":
        room.delete()
        return redirect('dashboard')
    context = {
        'obj':room
    }
    return render(request, 'room/delete_room.html', context)


def show_all_rooms(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'room/all_rooms.html', context)