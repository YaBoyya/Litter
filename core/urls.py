from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path('', views.feed, name="feed"),
    path('post/<str:pk>', views.post_details, name='details-post'),
    path('post/<str:pk>/edit', views.post_edit, name="edit-post"),
    path('create/', views.create_post, name="create-post"),
    path('delete/<str:pk>', views.delete_post, name="delete-post")
]
