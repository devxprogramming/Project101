from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    page = 'login_page'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
            
    context = {
        'page':page
    }
    return render(request, 'accounts/login_register.html', context)


def register_view(request):
    page = "register_page"
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            school_id = form.cleaned_data.get('school_id')
            full_name = form.cleaned_data.get('full_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, f'Hey {full_name}, your account has been successfully created')
            
            profile = Profile.objects.get(user=request.user)
            profile.full_name = full_name
            profile.gender = gender
            profile.password = password
            profile.school_id = school_id
            profile.save()

            return redirect('dashboard')

    context = {
        'page':page,
        'form':form
    }
    return render(request, 'accounts/login_register.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')