from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmailForm,    ProfileForm
from core.models import Post,  Comment
from users.models import LitterUser, UserFollowing


def profile_posts(request, usertag):
    posts = Post.objects.filter(user__usertag=usertag).all()
    user = get_object_or_404(LitterUser, usertag=usertag)
    is_followed = UserFollowing.objects.filter(user=request.user.id,
                                               followed_user=user).exists()

    context = {'posts': posts, 'user': user, 'is_followed': is_followed}
    return render(request, 'profiles/profile.html', context)


def profile_comments(request, usertag):
    comments = Comment.objects.filter(user__usertag=usertag).all()
    user = get_object_or_404(LitterUser, usertag=usertag)
    is_followed = UserFollowing.objects.filter(user=request.user.id,
                                               followed_user=user).exists()

    context = {'comments': comments, 'user': user, 'is_followed': is_followed}
    return render(request, 'profiles/profile.html', context)


@login_required(login_url='users:login')
def profile_following(request, usertag):
    """
    Will create a UserFollowing object,
    if it already exists it will be deleted
    """
    user_to_follow = get_object_or_404(LitterUser, usertag=usertag)
    try:
        follow = UserFollowing.objects.get(user=request.user.id,
                                           followed_user=user_to_follow)
    except (UserFollowing.DoesNotExist):
        follow = None

    if follow:
        follow.delete()
    else:
        UserFollowing.objects.create(user=request.user,
                                     followed_user=user_to_follow)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='users:login')
def profile_settings(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

    if request.user != user:
        return redirect('core:feed')
    return render(request, 'profiles/profile-settings.html', {'user': user})


# TODO make a decorator is_owner to check is request.user == user
@login_required(login_url='users:login')
def profile_edit(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

    if request.user != user:
        return redirect('core:feed')

    if request.method != 'POST':
        return render(request, 'profiles/profile-edit.html',
                      {'form': ProfileForm(instance=user)})

    form = ProfileForm(request.POST, instance=user)
    if not form.is_valid():
        messages.info(request, "Profile information is not valid.")
        return redirect(request.path_info)

    form.save()
    return redirect('profiles:posts', user.usertag)


@login_required(login_url='users:login')
def email_change(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

    if request.user != user:
        return redirect('core:feed')

    if request.method != 'POST':
        return render(request, 'profiles/profile-edit.html',
                      {'form': EmailForm(instance=user)})

    form = EmailForm(request.POST, instance=user)
    # TODO email confirmation?
    if not form.is_valid():
        messages.info(request, "Invalid email.")
        return redirect(request.path_info)

    form.save()
    return redirect('profiles:posts', usertag)


@login_required(login_url='users:login')
def password_change(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

    if request.user != user:
        return redirect('core:feed')

    if request.method != 'POST':
        return render(request, 'profiles/profile-edit.html',
                      {'form': PasswordChangeForm(user=user)})

    form = PasswordChangeForm(user, request.POST)
    if not form.is_valid():
        messages.info(request, "Invalid password.")
        (form.errors)
        return redirect(request.path_info)

    user = form.save()
    update_session_auth_hash(request, user)
    return redirect('profiles:posts', usertag)
