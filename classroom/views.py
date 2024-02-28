from django.shortcuts import render, redirect, get_object_or_404
from classroom.forms import RoomForm
from classroom.models import Room
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
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
            messages.success(request, 'Room created successfully')
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
            messages.success(request, 'Room updated successfully')
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
        messages.success(request, 'Room deleted successfully')
        return redirect('dashboard')
    context = {
        'obj':room
    }
    return render(request, 'room/delete_room.html', context)


def show_all_rooms(request):
    room = Room.objects.all()
    paginator = Paginator(room, 10)
    page = request.GET.get('page')
    rooms = paginator.get_page(page)
    context = {
        'rooms': rooms
        # 'page':page,
    }
    return render(request, 'room/all_rooms.html', context)