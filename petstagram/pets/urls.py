from django.urls import path

urlpatterns = [
    path('add/', add_pet, name='add pet'),
    path('<str:username>/pet/<slug:pet_name>/', details_pet, name='details pet'),
    path('<str:username>/pet/<slug:pet_name>/edit/', edit_pet, name='edit pet'),
    path('<str:username>/pet/<slug:pet_name>/delete/', delete_pet, name='delete pet')
]