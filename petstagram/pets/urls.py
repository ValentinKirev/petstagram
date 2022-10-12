from django.urls import path

from petstagram.pets.views import add_pet, details_pet, edit_pet, delete_pet

urlpatterns = [
    path('add/', add_pet, name='add pet'),
    path('<str:username>/pet/<slug:slug>/', details_pet, name='details pet'),
    path('<str:username>/pet/<slug:slug>/edit/', edit_pet, name='edit pet'),
    path('<str:username>/pet/<slug:slug>/delete/', delete_pet, name='delete pet')
]
