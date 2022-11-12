from django.contrib.auth.decorators import login_required
from django.urls import path

from petstagram.photos.views import PhotoAddView, PhotoDetailsView, PhotoEditView, PhotoDeleteView

urlpatterns = [
    path('add/', login_required(PhotoAddView.as_view()), name='add photo'),
    path('<int:pk>/', PhotoDetailsView.as_view(), name='details photo'),
    path('<int:pk>/edit/', PhotoEditView.as_view(), name='edit photo'),
    path('<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete photo'),
]
