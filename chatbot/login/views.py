from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sessions.backends.db import SessionStore
from .models import CustomUser
from django.utils import timezone

def create_session(request, user=None):
    request.session['username'] = user.username
    request.session['user_id'] = user.id

def check_username_exists(request, username):
    if CustomUser.objects.filter(username=username).exists():
        message = f"{username} already exists.."
        return render(request, 'signup.html', {'error': message})

def check_email_exists(request, email):
    if CustomUser.objects.filter(email=email).exists():
        message = f"Entered email already registered..."
        return render(request, 'signup.html', {'error': message})


def create_login(request):
    if request.POST:
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        print(f'{user_name = }, {password = }')
        
        if not user_name or not password:
            message = 'Username and Password required..'               # ------------>>> Use front end to handle this...
            return render(request, 'login.html', {'error': message})
        
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            create_session(request, user=user)
            return redirect('chat')
        else:
            message = 'Usernname and Password are not valid.'
            return render(request, 'login.html', {'error': message})

    return render(request, 'login.html')

def create_signup(request):
    if request.POST:
        user_name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        print(f'{user_name = }, {password = }, {email = }')

        check_username_exists(request, user_name)
        check_email_exists(request, email)
        
        try:
            user_obj = CustomUser(username=user_name, email=email)
            user_obj.set_password(password)
            user_obj.save()
            create_session(request, username=user_name)
            print('model is saved ....')
        except Exception:
            message = f"Your entered details are violating login rules.."
            return render(request, 'signup.html', {'error': message})
        print('redirecting...')
        return redirect('chat')
    return render(request, 'signup.html')

def create_logout(request):
    logout(request)
    return redirect('login')