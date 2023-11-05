from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegisterForm, LoginForm
from .models import LitterUser
from .tokens import account_activation_token


# TODO email activation later on
def register(request):
    type = 'register'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST.get('usertag')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link for your litter account.'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'users/please_activate.html')
    else:
        form = RegisterForm()
    context = {'form': form, 'type': type}
    return render(request, 'users/login-register.html', context)


def activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(LitterUser, id=uid)
    except (TypeError, ValueError, OverflowError, LitterUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank you for email activation.")
    else:
        return HttpResponse("Activation link is invalid.")


def user_login(request):
    type = 'login'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        next = request.GET.get('next', 'core:feed')
        user = authenticate(request,
                            usertag=request.POST.get('usertag'),
                            password=request.POST.get('password'))
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, "Logged in succesfully.")
            return redirect(next)
        elif not user.is_active:
            messages.info(request,
                          "Please activate your account before logging in.")
        else:
            messages.info(request, "Invalid usertag or password.")
    else:
        form = LoginForm()
    context = {'form': form, 'type': type}
    return render(request, 'users/login-register.html', context)


def user_logout(request):
    logout(request)
    return redirect('core:feed')
