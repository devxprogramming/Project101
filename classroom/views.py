import mimetypes
import re
from django.shortcuts import render, redirect, get_object_or_404
from classroom.forms import RoomForm, MessageForm, ResourceForm
from classroom.models import Room, Message, Resource, StudyAi
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.static import serve
import os
from django.http import FileResponse, Http404, HttpResponse
from core.settings import BASE_DIR
from IPython.display import Markdown
import textwrap
from IPython.display import display
import pathlib
from django.utils.safestring import mark_safe


# Ai imports
import dotenv
import google.generativeai as genai

# load env file
dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')

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

def delete_all_rooms(request):
    get_all_rooms = Room.objects.all()
    get_all_rooms.delete()
    return redirect('all_rooms')


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
    get_other_messages = Message.objects.filter(room=room).exclude(user=request.user).order_by('-created')
    participants = room.participants.all()
    get_all_messages = Message.objects.filter(room=room).order_by('-created')
    resources = room.resources.all()
    message_form = MessageForm()
    current_user_messages = Message.objects.filter(user=request.user, room=room).order_by('-created')
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
        'get_other_messages':get_other_messages,
        "participants":participants,
        "resources":resources,
        "current_user_messages":current_user_messages,
        "get_all_messages":get_all_messages,
    }
    return render(request, 'room/room_message.html', context)


def delete_message(request,pk):
    get_message = get_object_or_404(Message, message_code=pk)
    get_message.delete()
    return redirect(room_message, get_message.room.room_code)




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




def download_reference_material(request, pk):
    try:
        reference_material = Resource.objects.get(id=pk)
    except Resource.DoesNotExist:
        return HttpResponse('Reference material not found.')

    file_path = reference_material.upload.path
    file_name = reference_material.upload.name.split('/')[-1]

    # Get the file extension based on the MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        extension = mimetypes.guess_extension(mime_type)
        if extension:
            file_name = f"{file_name.split('.')[0]}{extension}"

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response




@login_required(login_url='login')
def use_ai(request):
    if request.method == "POST":
        userInput = request.POST.get('user-input')
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(userInput)

        # Extract the generated text from the response object
        generated_text = response.text

        # Replace bullet points with Markdown formatted lists
        generated_text = generated_text.replace('•', '*')

        # Make any next line go on a next line
        generated_text = generated_text.replace('**', '  ')



        # Pass the generated text to the to_markdown function
        output = generated_text
        
        # Saving the generated text to a file
        #  if file exist, add the next generated text, else create a new file with the generated text
        file_path = os.path.join(BASE_DIR, 'studdyai/generated_text.txt')
        if os.path.exists(file_path):
            with open(file_path, 'a') as f:
                f.write(f'\n\n{generated_text}')
        else:
            with open(file_path, 'w') as f:
                f.write(generated_text)
                
        # Saving to Database
        StudyAi.objects.create(
            user = request.user,
            prompt = userInput,
            response = output,
        ).save()
        
        your_history = StudyAi.objects.filter(user=request.user).order_by('-created')
        
        

        context={
            'response': output,
            "history":your_history,
        }
        return render(request, 'room/use_ai.html', context)
    else:
        your_history = StudyAi.objects.filter(user=request.user).order_by('-created')
        context={
            "history":your_history,
        }
        # Handle GET request
        return render(request, 'room/use_ai.html', context)