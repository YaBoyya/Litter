from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'core/feed.html', context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'core/create_post.html', context)
