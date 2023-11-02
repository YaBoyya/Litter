from django.shortcuts import render

from core.models import Post,  Comment
from users.models import LitterUser


# TODO profiles, settings and others
def profile_posts(request, usertag):
    posts = Post.objects.filter(user__usertag=usertag).all()
    user = LitterUser.objects.get(usertag=usertag)

    context = {'posts': posts, 'user': user}
    return render(request, 'profiles/profile-posts.html', context)


# TODO add buttons for changing feeds
def profile_comments(request, usertag):
    comments = Comment.objects.filter(user__usertag=usertag).all()
    user = LitterUser.objects.get(usertag=usertag)

    context = {'comments': comments, 'user': user}
    return render(request, 'profiles/profile-comments.html', context)
