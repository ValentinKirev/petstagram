from django.shortcuts import render, redirect

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import CreatePetForm, EditPetForm, DeletePetForm
from petstagram.pets.models import Pet


def add_pet(request):
    add_pet_form = CreatePetForm(request.POST or None)

    if add_pet_form.is_valid():
        add_pet_form.save()
        return redirect('details user', pk=1)

    context = {
        'form': add_pet_form
    }

    return render(request, 'pets/pet-add-page.html', context)


def details_pet(request, username, slug):
    pet = Pet.objects.get(slug=slug)
    all_photos = pet.photo_set.all()
    comment_form = CommentForm()

    context = {
        'pet': pet,
        'pet_photos': all_photos,
        'pet_photos_count': all_photos.count(),
        'comment_form': comment_form
    }

    return render(request, 'pets/pet-details-page.html', context)


def edit_pet(request, username, slug):
    pet = Pet.objects.filter(slug=slug).\
        get()

    if request.method == "GET":
        edit_pet_form = EditPetForm(instance=pet)
    else:
        edit_pet_form = EditPetForm(request.POST, instance=pet)

        if edit_pet_form.is_valid():
            edit_pet_form.save()
            return redirect('details pet', username, slug)

    context = {
        'form': edit_pet_form,
        'username': username,
        'slug': slug
    }

    return render(request, 'pets/pet-edit-page.html', context)


def delete_pet(request, username, slug):
    pet = Pet.objects.filter(slug=slug).\
        get()

    if request.method == "POST":
        pet.delete()
        return redirect('details user', pk=1)

    delete_pet_form = DeletePetForm(instance=pet)

    context = {
        'form': delete_pet_form,
        'username': username,
        'slug': slug
    }

    return render(request, 'pets/pet-delete-page.html', context)
