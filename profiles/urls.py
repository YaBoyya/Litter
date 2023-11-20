from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('<str:usertag>', views.profile_posts, name='posts'),
    path('<str:usertag>/comments', views.profile_comments, name='comments'),
    path('<str:usertag>/follow', views.profile_following, name='follow'),

    path('<str:usertag>/notifications', views.notification_list,
         name='notifications'),
    path('<str:usertag>/notification/<str:pk>/delete',
         views.notification_delete,
         name="notification-delete"),
    path('<str:usertag>/notification/delete-read',
         views.notification_delete_read,
         name="notification-delete-read"),
    path('<str:usertag>/notification/read-all',
         views.notification_read_all,
         name="notification-read-all"),
    path('<str:usertag>/notification/<str:pk>/redirect',
         views.notification_redirect,
         name="notification-redirect"),

    path('<str:usertag>/settings', views.profile_settings, name='settings'),
    path('<str:usertag>/settings/profile-edit',
         views.profile_edit, name='edit'),
    path('<str:usertag>/settings/email-change',
         views.email_change, name='email-change'),
    path('<str:usertag>/settings/password-change',
         views.password_change, name='password-change'),
    path('<str:usertag>/settings/language-follow',
         views.language_follow, name='language-follow'),
]
