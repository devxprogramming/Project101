from django.shortcuts import render, redirect
from accounts.models import User, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"You are already looged In. Welcome back {request.user}")
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
        except User.DoesNotExist:
            messages.info(request, 'Invalid username or password')
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
    user = request.user
    logout(request)
    messages.success(request, f'{user} Logged out Successfully')
    return redirect('login')


def user_profile(request, pk):
    profile = User.objects.get(school_id=pk)
    user = User.objects.all()
    
    context = {
        'profile':profile,
        'user':user
    }
    return render(request, 'accounts/user_profile.html', context)


def change_password(request):
    page = "change_password"
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/user_profile.html', {
        'form': form,
        "page":page,
    })