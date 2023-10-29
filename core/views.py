from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import author_only
from .forms import PostForm, CommentForm
from .models import Comment, CommentVote, Post, PostVote


def feed(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'core/feed.html', context)


# TODO separate comment form
def post_details(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.post = post
            obj.save()

    form = CommentForm()

    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'core/details_post.html', context)


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot edit this post")
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


@login_required(login_url='users:login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('core:feed')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'core/create_post.html', context)


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot delete this post.")
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('core:feed')
    context = {'obj': post}
    return render(request, 'delete.html', context)


# TODO a generic view for voting?
@login_required(login_url='users:login')
def vote_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    try:
        vote = PostVote.objects.get(user=request.user, post=post)
    except (PostVote.DoesNotExist):
        vote = None

    if vote:
        vote.delete()
    else:
        PostVote.objects.create(user=request.user, post=post)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='users:login')
def vote_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    try:
        vote = CommentVote.objects.get(user=request.user, comment=comment)
    except (CommentVote.DoesNotExist):
        vote = None

    if vote:
        vote.delete()
    else:
        CommentVote.objects.create(user=request.user, comment=comment)

    return redirect(request.META.get('HTTP_REFERER'))
