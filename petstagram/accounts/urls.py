from django.urls import path

from petstagram.accounts.views import details_user, edit_user, delete_user, SignUpView, SignInView, SignOutView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register user'),
    path('login/', SignInView.as_view(), name='login user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', details_user, name='details user'),
    path('profile/<int:pk>/edit/', edit_user, name='edit user'),
    path('profile/<int:pk>/delete/', delete_user, name='delete user')
]
