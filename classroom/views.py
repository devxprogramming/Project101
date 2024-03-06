from django.shortcuts import render, redirect, get_object_or_404
from classroom.forms import RoomForm, MessageForm, ResourceForm
from classroom.models import Room, Message, Resource
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
            course_code = form.cleaned_data['course_code']
            course_title = form.cleaned_data['course_title']
            participants = form.cleaned_data['participants']
            resource = form.cleaned_data["resources"]

            
            if Room.objects.filter(course_code=course_code).exists():
                messages.info(request, 'Course Code already exists')
                return redirect('create_room')
            elif Room.objects.filter(course_title=course_title).exists():
                messages.info(request, 'Course Title already exists')
                return redirect('create_room')
            room = form.save(commit=False)        
            room.host = request.user
            room.check_password(password)
            room.save()
            
            # Save Participants
            participants = form.cleaned_data.get('participants')
            room.participants.set(participants)

            # Save resources
            resources = form.cleaned_data.get('resources')
            room.resources.set(resources)
            
            
            
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
    paginator = Paginator(room, 6)
    page = request.GET.get('page')
    rooms = paginator.get_page(page)
    room_count = Room.objects.all().count()
    context = {
        'rooms': rooms,
        'room_count':room_count,
        # 'page':page,
    }
    return render(request, 'room/all_rooms.html', context)

@login_required(login_url='login')
def room_message(request, pk):
    room = get_object_or_404(Room, room_code=pk)
    get_messages = Message.objects.filter(room=room)
    participants = room.participants.all()
    resources = room.resources.all()
    message_form = MessageForm()
    if request.method == "POST":
        room_messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') 
        )
        room.participants.add(request.user)
        return redirect('room_message', pk)
        
    context = {
        'room':room,
        'message_form':message_form,
        'get_messages':get_messages,
        "participants":participants,
        "resources":resources,
    }
    return render(request, 'room/room_message.html', context)


def delete_message(request,pk):
    get_message = get_object_or_404(Message, message_code=pk)
    if request.method == "POST":
        get_message.delete()
        messages.success(request, 'Message deleted Success')
        return redirect(room_message, get_message.room.room_code)
    context = {
        "obj":get_message
    }
    return render(request, 'base/delete.html', context)




def create_resources(request):
    form = ResourceForm()
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            resource = form.save(commit=False)
            resource.author = request.user
            if Resource.objects.filter(filename=filename).exists():
                messages.info(request, 'Resource already exists')
                return redirect('create_resources')
            resource.save()
            messages.success(request, 'Resource created successfully')
            return redirect('dashboard')
        
    context = {
        'form':form
    }
    return render(request, 'resources/create_resources.html', context)