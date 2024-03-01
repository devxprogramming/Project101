from django.shortcuts import render, redirect
from django.contrib import messages
from classroom.models import Room
from accounts.models import User, Profile
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home_page(request):
    page = "dashboard"
    
    rooms = Room.objects.all()
    
    paginator = Paginator(rooms, 5)
    page = request.GET.get('page')
    paginate_room = paginator.get_page(page)
    
    lecturers = User.objects.filter(account_type='Lecturer')
    students = User.objects.filter(account_type='Student')
    profiles = Profile.objects.filter(user=request.user)
    context = {
        'page':page,
        'rooms': rooms,
        'lecturers': lecturers,
        "students":students,
        'profile': profiles,
        "paginate_room":paginate_room,
    }
    return render(request, 'dashboard/home.html', context)


def search_page(request):
    query = request.GET.get('query')
    rooms = Room.objects.filter(
        Q(course_code__icontains=query) |
        Q(course_title__icontains=query) |
        Q(host__school_id__icontains=query)
    ).order_by('-created')
   
    
    context = {
        'query':query,
        'rooms':rooms
    }
    return render(request, 'dashboard/search.html', context)