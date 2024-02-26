from django.shortcuts import render, redirect
from accounts.models import User, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already looged In")
        return redirect('dashboard')
    page = 'login_page'
    if request.method == 'POST':
        school_id = request.POST.get('school_id')
        password = request.POST.get('password')
        try:
            user = User.objects.get(school_id=school_id)
            user = authenticate(username=school_id, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successful')
                return redirect('dashboard')
            else:
                messages.info(request, 'Invalid username or password')
                return redirect('login')
        except:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
        
            
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
            newuser = form.save(commit=False)
            if 'LE' in request.POST['school_id']:
                newuser.account_type = 'Lecturer'
                newuser.save()
            else:
                newuser.account_type = 'Student'
                newuser.save()


            school_id = form.cleaned_data.get('school_id')
            full_name = form.cleaned_data.get('full_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password1')

            

            user = authenticate(username=school_id, password=password)
            login(request, user)

            messages.success(request, f'Hey {full_name}, your account has been successfully created')
            
            profile = Profile.objects.get(user=request.user)
            profile.full_name = full_name
            profile.gender = gender
            profile.password = password
            profile.school_id = school_id

            if 'LE' in request.POST['school_id']:
                profile.account_type = 'Lecturer'
                profile.save()
            else:
                profile.account_type = 'Student'
                profile.save()

            return redirect('dashboard')

    context = {
        'page':page,
        'form':form
    }
    return render(request, 'accounts/login_register.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out Successful')
    return redirect('login')


def user_profile(request):
    profile = Profile.objects.all()
    user = User.objects.all()
    
    context = {
        'profile':profile,
        'user':user
    }
    return render(request, 'accounts/user_profile.html', context)