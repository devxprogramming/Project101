from django.shortcuts import render, redirect
from django.contrib import messages
from classroom.models import Room
from accounts.models import User, Profile


def home_page(request):
    if request.user.is_authenticated:

        rooms = Room.objects.all()
        users = User.objects.all()
        profiles = Profile.objects.filter(user=request.user)
        context = {
            'rooms': rooms,
            'users': users,
            'profile': profiles
        }
        return render(request, 'dashboard/home.html', context)
    else:
        return redirect('login')