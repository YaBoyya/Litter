from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import author_only
from .forms import CommentForm, PostForm, SearchForm
from .models import Comment, CommentVote, Post, PostVote
from profiles.models import Notification


def feed(request, page='home', trend='hot'):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            post_form.save_m2m()
            return redirect('core:feed')

    if request.GET.get('q') is not None:
        request.session['q'] = request.GET.get('q')
        return redirect('core:search')

    posts = Post.objects.get_sorted_feed(user=request.user, sort=trend)

    if (not request.user.is_authenticated
            or not request.user.languages.exists()):
        page = 'popular'

    if page == 'home':
        posts = posts.filter(
            Q(user__languages__in=request.user.languages.all())
            | Q(user__in=request.user.following.all())
        )

    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'posts': page_obj, 'trend': trend,
               'page': page, 'form': PostForm()}
    return render(request, 'core/feed.html', context)


def search(request):
    form = SearchForm(request.GET, auto_id=False)
    q = request.session.pop('q', form.data.get('q', ''))
    trend = form.data.get('trend', '').lower()
    languages = form.data.getlist('languages', None)
    difficulty = form.data.get('difficulty', None)

    posts = Post.objects.get_sorted_feed(user=request.user, sort=trend)

    if q:
        posts = posts.filter(
                            Q(title__icontains=q)
                            | Q(text__icontains=q)
                            | Q(languages__name__istartswith=q)
                            ).order_by('-created')

    if difficulty:
        posts = posts.filter(difficulty=difficulty)

    if languages:
        posts = posts.filter(languages__name__in=languages)

    paginator = Paginator(posts, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'posts': page_obj, 'q': q, 'form': form}
    return render(request, 'core/search.html', context)


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot delete this post.")
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method != 'POST':
        return render(request, 'delete.html', {'obj': post})

    post.delete()
    return redirect('core:feed')


def post_details(request, pk):
    try:
        if request.user.is_authenticated:
            post = Post.objects.get_voted(request.user).get(id=pk)
            comments = Comment.objects.get_voted(request.user).filter(
                post=post).order_by('-created')
        else:
            post = Post.objects.get_voted().get(id=pk)
            comments = Comment.objects.get_voted().filter(
                post=post).order_by('-created')
    except (Post.DoesNotExist):
        messages.error(request, 'Post does not exist.')
        return redirect('core:feed')

    context = {'post': post, 'comments': comments, 'form': CommentForm()}
    if request.method != 'POST':
        post.views += 1
        post.save()
        return render(request, 'core/post-details.html', context)

    form = CommentForm(request.POST)
    if not form.is_valid():
        messages.info(request, "Your comment is invalid.")
        return redirect(request.path_info)

    obj = form.save(commit=False)
    obj.user = request.user
    obj.post = post
    obj.save()
    Notification.objects.create(
        recipient=post.user,
        sender=request.user,
        activity_type=Notification.COMMENT,
        object_type=Notification.COMMENT,
        object_url=f"{request.path_info}#{obj.id}"
    )
    return redirect('core:post-details', pk)


@login_required(login_url='users:login')
@author_only(obj=Post, message="You cannot edit this post")
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method != 'POST':
        return render(request, 'core/post-edit.html',
                      {'form': PostForm(instance=post)})

    form = PostForm(request.POST, instance=post)
    if not form.is_valid():
        messages.info(request, "Your post is invalid.")
        return redirect(request.path_info)
    obj = form.save(commit=False)
    obj.was_edited = True
    obj.save()
    form.save_m2m()
    return redirect('core:post-details', pk)


@login_required(login_url='users:login')
def post_vote(request, pk):
    post = get_object_or_404(Post, id=pk)
    try:
        vote = PostVote.objects.get(user=request.user, post=post)
    except (PostVote.DoesNotExist):
        vote = None

    if vote:
        vote.delete()
        Post.objects.filter(id=pk).update(total_votes=F("total_votes") - 1)
        return HttpResponse(status=200)

    PostVote.objects.create(user=request.user, post=post)
    Post.objects.filter(id=pk).update(total_votes=F("total_votes") + 1)
    return HttpResponse(status=200)


@login_required(login_url='users:login')
@author_only(obj=Comment, message="You cannot delete this comment.")
def comment_delete(request, pk):
    comment = Comment.objects.select_related('post').get(id=pk)
    post_id = comment.post.id
    if request.method != 'POST':
        return render(request, 'delete.html', {'obj': comment})

    comment.delete()
    return redirect('core:post-details', post_id)


@login_required(login_url='user:login')
@author_only(obj=Comment, message="You cannot edit this comment.")
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method != 'POST':
        return render(request, 'core/comment-edit.html',
                      {'form': CommentForm(instance=comment)})

    form = CommentForm(request.POST, instance=comment)
    if not form.is_valid():
        messages.info(request, "Your comment is invalid.")
        return redirect(request.path_info)

    obj = form.save(commit=False)
    obj.was_edited = True
    obj.save()
    return redirect('core:post-details', comment.post.id)


@login_required(login_url='users:login')
def comment_vote(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    try:
        vote = CommentVote.objects.get(user=request.user, comment=comment)
    except (CommentVote.DoesNotExist):
        vote = None

    if vote:
        vote.delete()
        Comment.objects.filter(id=pk).update(total_votes=F("total_votes") - 1)
        return HttpResponse(status=200)

    CommentVote.objects.create(user=request.user, comment=comment)
    Comment.objects.filter(id=pk).update(total_votes=F("total_votes") + 1)
    return HttpResponse(status=200)
