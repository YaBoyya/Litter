from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import author_only
from .forms import PostForm, CommentForm
from .models import Comment, CommentVote, Post, PostVote


def feed(request):
    q = request.GET.get('q', "")
    if q:
        posts = Post.objects.filter(Q(title__icontains=q)
                                    | Q(text__icontains=q)
                                    | Q(languages__name__icontains=q))
    else:
        posts = Post.objects.all().order_by('-created')
    context = {'posts': posts, 'q': q}
    return render(request, 'core/feed.html', context)


# TODO separate comment form
def post_details(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post).order_by('-created')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.post = post
            obj.save()
    else:
        post.views += 1
        post.save()

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
            obj = form.save(commit=False)
            obj.was_edited = True
            obj.save()
            form.save_m2m()
            # TODO change it signals?
            return redirect('core:details-post', pk)
    else:
        form = PostForm(instance=post)
    context = {'post': post, 'form': form}
    return render(request, 'edit.html', context)


@login_required(login_url='users:login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return redirect('core:feed')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'core/create_post.html', context)


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot delete this post.")
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('core:feed')
    context = {'obj': post}
    return render(request, 'delete.html', context)


@login_required(login_url='users:login')
@author_only(obj=Comment, message="You cannot delete this comment.")
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('core:details-post', post_id)
    context = {'obj': comment}
    return render(request, 'delete.html', context)


@login_required(login_url='user:login')
@author_only(obj=Comment, message="You cannot edit this comment.")
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            print(form)
            obj = form.save(commit=False)
            obj.was_edited = True
            obj.save()
            return redirect('core:details-post', comment.post.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'edit.html', context)


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
