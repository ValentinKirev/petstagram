from django.urls import path

from petstagram.accounts.views import *

urlpatterns = [
    path('register/', register_user, name='register user'),
    path('login/', login_user, name='login user'),
    path('profile/<int:pk>/', details_user, name='details user'),
    path('profile/<int:pk>/edit/', edit_user, name='edit user'),
    path('profile/<int:pk>/delete/', delete_user, name='delete user')
]
