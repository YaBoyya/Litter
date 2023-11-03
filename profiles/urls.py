from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('<str:usertag>/', views.profile_posts, name='posts'),
    path('<str:usertag>/comments', views.profile_comments, name='comments'),
    path('<str:usertag>/stats', views.profile_stats, name='stats'),
    path('<str:usertag>/follow', views.profile_following, name='follow'),
]
