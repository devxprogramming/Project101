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
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data['room_password']
            room = form.save(commit=False)
            room.host = request.user
            room.check_password(password)
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

@login_required(login_url="login")
def update_room(request, pk):
    if request.user != Room.objects.get(room_code=pk).host:
        return redirect('all_rooms')
    
    page = 'update_room'
    room = Room.objects.get(room_code=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room, files=request.FILES)
        if form.is_valid():
            room.check_password(form.cleaned_data['room_password'])
            form.save()
            messages.success(request, 'Room updated successfully')
            return redirect('all_rooms')
        
    context = {
        'page':page,
        'form':form,
    }
        
    return render(request, 'room/create_update.html', context)

@login_required(login_url='login')
def private_room(request, pk):
    if request.method == "POST":
        room = get_object_or_404(Room, room_code=pk)
        password = request.POST.get('password')
        if password == room.room_password:
            messages.success(request, 'Authorised')
            return redirect('update_room', pk)
        else:
            messages.info(request, 'Wrong password')
    return render(request, 'room/private_room.html')

@login_required(login_url='login')
def delete_room(request, pk):
    if request.user != Room.objects.get(room_code=pk).host:
        return redirect('all_rooms')
    room = Room.objects.get(room_code=pk)
    if request.method == "POST":
        room.delete()
        messages.success(request, 'Room deleted successfully')
        return redirect('all_rooms')
    context = {
        'obj':room
    }
    return render(request, 'room/delete_room.html', context)


def show_all_rooms(request):
    room = Room.objects.all()
    paginator = Paginator(room, 5)
    page = request.GET.get('page')
    rooms = paginator.get_page(page)
    context = {
        'rooms': rooms
        # 'page':page,
    }
    return render(request, 'room/all_rooms.html', context)