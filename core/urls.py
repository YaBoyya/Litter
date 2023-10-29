from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path('', views.feed, name="feed"),
    path('create/', views.create_post, name="create-post"),
    path('post/<str:pk>', views.post_details, name='details-post'),
    path('post/<str:pk>/edit', views.post_edit, name="edit-post"),
    path('post/<str:pk>/delete', views.delete_post, name="delete-post")
]
