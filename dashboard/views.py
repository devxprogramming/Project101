from django.shortcuts import render, redirect
from django.contrib import messages
from classroom.models import Room
from accounts.models import User, Profile
from django.core.paginator import Paginator


def home_page(request):
    if request.user.is_authenticated:

        rooms = Room.objects.all().order_by('-created')
        paginator = Paginator(rooms, 5)
        page = request.GET.get('page')
        paginate_room = paginator.get_page(page)
        
        lecturers = User.objects.filter(account_type='Lecturer')
        students = User.objects.filter(account_type='Student')
        profiles = Profile.objects.filter(user=request.user)
        context = {
            'rooms': rooms,
            'lecturers': lecturers,
            "students":students,
            'profile': profiles,
            "paginate_room":paginate_room,
        }
        return render(request, 'dashboard/home.html', context)
    else:
        return redirect('login')