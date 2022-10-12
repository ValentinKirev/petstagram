from django.shortcuts import render

from petstagram.pets.models import Pet


def add_pet(request):
    return render(request, 'pets/pet-add-page.html')


def details_pet(request, username, slug):
    pet = Pet.objects.get(slug=slug)
    all_photos = pet.photo_set.all()

    context = {
        'pet': pet,
        'pet_photos': all_photos,
        'pet_photos_count': all_photos.count()
    }

    return render(request, 'pets/pet-details-page.html', context)


def edit_pet(request, username, slug):
    return render(request, 'pets/pet-edit-page.html')


def delete_pet(request, username, slug):
    return render(request, 'pets/pet-delete-page.html')
