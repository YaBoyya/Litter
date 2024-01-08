from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('u/<str:usertag>', views.profile_posts, name='posts'),
    path('u/<str:usertag>/comments', views.profile_comments, name='comments'),
    path('u/<str:usertag>/follow', views.profile_following, name='follow'),

    path('u/<str:usertag>/notifications', views.notification_list,
         name='notifications'),
    path('u/<str:usertag>/notifications/<str:pk>/delete',
         views.notification_delete,
         name="notification-delete"),
    path('u/<str:usertag>/notifications/delete-read',
         views.notification_delete_read,
         name="notification-delete-read"),
    path('u/<str:usertag>/notifications/read-all',
         views.notification_read_all,
         name="notification-read-all"),
    path('u/<str:usertag>/notifications/<str:pk>/redirect',
         views.notification_redirect,
         name="notification-redirect"),

    path('u/<str:usertag>/settings', views.profile_settings, name='settings'),
    path('u/<str:usertag>/settings/profile-edit',
         views.profile_edit, name='edit'),
    path('u/<str:usertag>/settings/email-change',
         views.email_change, name='email-change'),
    path('u/<str:usertag>/settings/password-change',
         views.password_change, name='password-change'),
    path('u/<str:usertag>/settings/language-follow',
         views.language_follow, name='language-follow'),
]
