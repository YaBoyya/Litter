from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('<str:usertag>', views.profile_posts, name='posts'),
    path('<str:usertag>/comments', views.profile_comments, name='comments'),
    path('<str:usertag>/follow', views.profile_following, name='follow'),

    path('<str:usertag>/settings', views.profile_settings, name='settings'),
    path('<str:usertag>/settings/profile-edit',
         views.profile_edit, name='edit'),
    path('<str:usertag>/settings/email-change',
         views.email_change, name='email-change'),
    path('<str:usertag>/settings/password-change',
         views.password_change, name='password-change'),
]
