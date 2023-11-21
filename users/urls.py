from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('delete', views.user_delete, name="delete"),
    path('activation/<uidb64>/<token>', views.activation, name="activation"),
]
