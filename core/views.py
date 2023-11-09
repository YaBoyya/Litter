from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import author_only
from .forms import PostForm, CommentForm
from .models import Comment, CommentVote, Post, PostVote


def feed(request):
    # TODO multiple images per post
    q = request.GET.get('q', "")
    if q:
        posts = Post.objects.filter(Q(title__icontains=q)
                                    | Q(text__icontains=q)
                                    | Q(languages__name__icontains=q))
    else:
        posts = Post.objects.select_related('user').all().order_by('-created')
    context = {'posts': posts, 'q': q}
    return render(request, 'core/feed.html', context)


# TODO separate comment form
def post_details(request, pk):
    post = Post.objects.prefetch_related('comment').get(id=pk)
    context = {'post': post, 'form': CommentForm()}
    if request.method != 'POST':
        post.views += 1
        post.save()
        return render(request, 'core/details_post.html', context)

    form = CommentForm(request.POST)
    if not form.is_valid():
        messages.info(request, "Your comment is invalid.")
        return redirect(request.path_info)

    obj = form.save(commit=False)
    obj.user = request.user
    obj.post = post
    obj.save()
    context.update({'form': form})
    return render(request, 'core/details_post.html', context)


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot edit this post")
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    context = {'post': post}
    if request.method != 'POST':
        context.update({'form': PostForm(instance=post)})
        return render(request, 'edit.html', context)

    form = PostForm(request.POST, instance=post)
    if not form.is_valid():
        messages.infor(request, "Your post is invalid.")
        return redirect(request.path_info)
    obj = form.save(commit=False)
    obj.was_edited = True
    obj.save()
    form.save_m2m()
    # TODO change it signals?
    return redirect('core:details-post', pk)


@login_required(login_url='users:login')
def create_post(request):
    if request.method != 'POST':
        return render(request, 'core/create_post.html', {'form': PostForm()})

    form = PostForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.info(request, "Your post is invalid.")
        return redirect(request.path_info)
    print(form.cleaned_data)
    post = form.save(commit=False)
    post.user = request.user
    post.save()
    form.save_m2m()
    return redirect('core:feed')


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot delete this post.")
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method != 'POST':
        return render(request, 'delete.html', {'obj': post})

    post.delete()
    return redirect('core:feed')


@login_required(login_url='users:login')
@author_only(obj=Comment, message="You cannot delete this comment.")
def delete_comment(request, pk):
    comment = Comment.objects.select_related('post').get(id=pk)
    post_id = comment.post.id
    if request.method != 'POST':
        return render(request, 'delete.html', {'obj': comment})

    comment.delete()
    return redirect('core:details-post', post_id)


@login_required(login_url='user:login')
@author_only(obj=Comment, message="You cannot edit this comment.")
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method != 'POST':
        return render(request, 'edit.html',
                      {'form': CommentForm(instance=comment)})

    form = CommentForm(request.POST, instance=comment)
    if not form.is_valid():
        messages.info(request, "Your comment is invalid.")
        return redirect(request.path_info)

    obj = form.save(commit=False)
    obj.was_edited = True
    obj.save()
    return redirect('core:details-post', comment.post.id)


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
