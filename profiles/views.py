from django.shortcuts import get_object_or_404, redirect, render

from core.models import Post,  Comment
from users.models import LitterUser, UserFollowing


# TODO settings and others
def profile_posts(request, usertag):
    posts = Post.objects.filter(user__usertag=usertag).all()
    user = get_object_or_404(LitterUser, usertag=usertag)
    is_followed = UserFollowing.objects.filter(user=request.user.id,
                                               followed_user=user).exists()

    context = {'posts': posts, 'user': user, 'is_followed': is_followed}
    return render(request, 'profiles/profile-posts.html', context)


def profile_comments(request, usertag):
    comments = Comment.objects.filter(user__usertag=usertag).all()
    user = get_object_or_404(LitterUser, usertag=usertag)
    is_followed = UserFollowing.objects.filter(user=request.user.id,
                                               followed_user=user).exists()

    context = {'comments': comments, 'user': user, 'is_followed': is_followed}
    return render(request, 'profiles/profile-comments.html', context)


# TODO profile stats
def profile_stats(request, usertag):
    pass


# TODO post template
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
