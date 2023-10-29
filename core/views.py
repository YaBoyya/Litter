from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post, Comment


def feed(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'core/feed.html', context)


def post_details(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)

    context = {'post': post, 'comments': comments}
    return render(request, 'core/details_post.html', context)


def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('core:details-post', pk)
    else:
        form = PostForm(instance=post)
    context = {'post': post, 'form': form}
    return render(request, 'core/edit_post.html', context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:feed')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'create_post.html', context)


def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('core:feed')
    context = {'obj': post}
    return render(request, 'delete.html', context)
