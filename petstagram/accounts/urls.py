from django.urls import path

from petstagram.accounts.views import SignUpView, SignInView, SignOutView, UserEditView, UserDetailsView, UserDeleteView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register user'),
    path('login/', SignInView.as_view(), name='login user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', UserDetailsView.as_view(), name='details user'),
    path('profile/<int:pk>/edit/', UserEditView.as_view(), name='edit user'),
    path('profile/<int:pk>/delete/', UserDeleteView.as_view(), name='delete user')
]
