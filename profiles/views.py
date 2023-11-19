from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .decorators import owner_only
from .forms import EmailForm, LanguageTagForm, ProfileForm
from .models import Notification
from core.models import Post, Comment
from users.models import LitterUser, UserFollowing


def profile_posts(request, usertag):
    posts = Post.objects.filter(user__usertag=usertag).all()
    user = get_object_or_404(LitterUser, usertag=usertag)
    post_points = posts.aggregate(pts=models.Sum('vote_count'))
    comment_points = Comment.objects.filter(
        user__usertag=usertag).aggregate(pts=models.Sum('vote_count'))
    points = post_points['pts'] + comment_points['pts']

    is_followed = UserFollowing.objects.filter(user=request.user.id,
                                               followed_user=user).exists()

    context = {'posts': posts, 'user': user,
               'is_followed': is_followed, 'points': points}
    return render(request, 'profiles/profile.html', context)


def profile_comments(request, usertag):
    comments = Comment.objects.filter(user__usertag=usertag).all()

    post_points = Post.objects.filter(
        user__usertag=usertag).aggregate(pts=models.Sum('vote_count'))
    comment_points = comments.aggregate(pts=models.Sum('vote_count'))
    points = post_points['pts'] + comment_points['pts']

    user = get_object_or_404(LitterUser, usertag=usertag)
    is_followed = UserFollowing.objects.filter(user=request.user.id,
                                               followed_user=user).exists()

    context = {'comments': comments, 'user': user,
               'is_followed': is_followed, 'points': points}
    return render(request, 'profiles/profile.html', context)


@login_required(login_url='users:login')
def profile_following(request, usertag):
    """
    Will create a UserFollowing object,
    if it already exists it will be deleted
    """
    # TODO AJAX this
    user_to_follow = get_object_or_404(LitterUser, usertag=usertag)
    try:
        follow = UserFollowing.objects.get(user=request.user.id,
                                           followed_user=user_to_follow)
    except (UserFollowing.DoesNotExist):
        follow = None

    print(reverse('profiles:posts', kwargs={'usertag': request.user.usertag}))
    if follow:
        follow.delete()
    else:
        UserFollowing.objects.create(user=request.user,
                                     followed_user=user_to_follow)
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            activity_type=Notification.FOLLOW,
            object_type=Notification.FOLLOW,
            object_url=reverse('profiles:posts',
                               kwargs={'usertag': request.user.usertag})
        )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='users:login')
@owner_only()
def profile_settings(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)
    return render(request, 'profiles/profile-settings.html', {'user': user})


@login_required(login_url='users:login')
@owner_only()
def profile_edit(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

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
@owner_only()
def email_change(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

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
@owner_only()
def password_change(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

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


@login_required(login_url='users:login')
@owner_only()
def language_follow(request, usertag):
    user = get_object_or_404(LitterUser, usertag=usertag)

    if request.method != 'POST':
        return render(request, 'profiles/profile-edit.html',
                      {'form': LanguageTagForm(instance=user)})

    form = LanguageTagForm(request.POST, instance=user)
    if not form.is_valid():
        messages.info(request, "Something went wrong.")
        return redirect(request.path_info)
# TODO notification system
    form.save()
    return redirect('profiles:posts', usertag)


@login_required(login_url='users:login')
@owner_only()
def notification_list(request, usertag):
    notifications = Notification.objects.filter(recipient__usertag=usertag)
    context = {'notifications': notifications}
    return render(request, 'profiles/notification-list.html', context)


@login_required(login_url='users:login')
@owner_only()
def notification_delete(request, usertag, pk):
    # TODO AJAX this
    notif = get_object_or_404(Notification, id=pk)
    notif.delete()
    return redirect('profiles:notifications', usertag)


@login_required(login_url='users:login')
@owner_only()
def notification_delete_read(request, usertag):
    # TODO AJAX this
    Notification.objects.filter(recipient=request.user,
                                is_unread=False).delete()
    return redirect('profiles:notifications', usertag)


@login_required(login_url='users:login')
@owner_only()
def notification_redirect(request, usertag, pk):
    # TODO add ids to comments for more precise redirects
    notif = get_object_or_404(Notification, id=pk)
    notif.is_unread = False
    notif.save()
    return redirect(notif.object_url)
