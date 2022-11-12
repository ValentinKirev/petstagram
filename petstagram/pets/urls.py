from django.contrib.auth.decorators import login_required
from django.urls import path

from petstagram.pets.views import PetAddView, PetDetailView, PetEditView, PetDeleteView

urlpatterns = [
    path('add/', login_required(PetAddView.as_view()), name='add pet'),
    path('<str:username>/pet/<slug:slug>/', PetDetailView.as_view(), name='details pet'),
    path('<str:username>/pet/<slug:slug>/edit/', PetEditView.as_view(), name='edit pet'),
    path('<str:username>/pet/<slug:slug>/delete/', PetDeleteView.as_view(), name='delete pet')
]
