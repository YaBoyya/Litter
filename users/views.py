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


def register(request):
    type = 'register'
    context = {'type': type}
    if request.method != 'POST':
        context.update({'form': RegisterForm()})
        return render(request, 'users/login-register.html', context)

    form = RegisterForm(request.POST)

    if not form.is_valid():
        messages.info(request, "Invalid registration info.")
        return redirect(request.path_info)

    user = form.save(commit=False)
    user.username = request.POST.get('usertag')
    user.is_active = False
    user.save()
    current_site = get_current_site(request)
    mail_subject = 'Activation link for your litter account.'
    message = render_to_string('users/account-activation-email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = form.cleaned_data['email']
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    return render(request, 'users/please-activate.html')


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
    context = {'type': type, 'form': LoginForm()}
    if request.method != 'POST':
        return render(request, 'users/login-register.html', context)

    next = request.GET.get('next', 'core:feed')
    user = authenticate(request,
                        usertag=request.POST.get('usertag'),
                        password=request.POST.get('password'))
    if user is None:
        messages.info(request, "Invalid usertag or password.")
    elif not user.is_active:
        messages.info(request,
                      "Please activate your account before logging in.")
    else:
        login(request, user)
        messages.success(request, "Logged in succesfully.")
        return redirect(next)
    return render(request, 'users/login-register.html', context)


def user_logout(request):
    logout(request)
    return redirect('core:feed')


def user_delete(request):
    if request.method != 'POST':
        return render(request, 'delete.html', {'obj': request.user.usertag})
    request.user.delete()
    return redirect('core:feed')
