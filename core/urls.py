from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path('', views.feed, name="feed"),
    path('filter/<str:trend>', views.feed, name="feed-filtered"),

    path('post/<str:pk>', views.post_details, name='post-details'),
    path('post/<str:pk>/edit', views.post_edit, name="post-edit"),
    path('post/<str:pk>/delete', views.post_delete, name="post-delete"),
    path('post/<str:pk>/vote', views.post_vote, name='post-vote'),

    path('comment/<str:pk>/edit', views.comment_edit, name="comment-edit"),
    path('comment/<str:pk>/delete', views.comment_delete,
         name='comment-delete'),
    path('comment/<str:pk>/vote', views.comment_vote, name='comment-vote'),
]
