from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def home(request):
    return render(request, 'tasks/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'tasks/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentTasks')
            except IntegrityError:
                    return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'tasks/loginuser.html', {'form':AuthenticationForm()})
    else:
       user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
    else:
        login(request, user)
        return redirect('currentTasks')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currentTasks(request):
    #tasks = tasks.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks/currentTasks.html')


