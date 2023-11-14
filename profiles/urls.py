from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('<str:usertag>', views.profile_posts, name='posts'),
    path('<str:usertag>/comments', views.profile_comments, name='comments'),
    path('<str:usertag>/stats', views.profile_stats, name='stats'),
    path('<str:usertag>/follow', views.profile_following, name='follow'),
    path('<str:usertag>/settings', views.profile_settings, name='settings'),
    path('<str:usertag>/edit', views.profile_edit, name='edit'),
]
