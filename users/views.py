from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm
# from .models import LitterUser


# TODO email activation later on
def register(request):
    type = 'register'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.usertag
            user.save()
            return redirect('core:feed')
    else:
        form = RegisterForm()
    context = {'form': form, 'type': type}
    return render(request, 'users/login-register.html', context)


def user_login(request):
    type = 'login'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(request,
                            usertag=request.POST.get('usertag'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in succesfully.")
            return redirect('core:feed')
        else:
            messages.info(request, "Invalid usertag or password.")
    else:
        form = LoginForm()
    context = {'form': form, 'type': type}
    return render(request, 'users/login-register.html', context)


def user_logout(request):
    logout(request)
    return redirect('core:feed')
