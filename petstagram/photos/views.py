from django.shortcuts import render, redirect

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import CreatePhotoForm, EditPhotoForm
from petstagram.photos.models import Photo


def add_photo(request):
    add_photo_form = CreatePhotoForm(request.POST or None, request.FILES or None)

    if add_photo_form.is_valid():
        photo = add_photo_form.save(commit=False)
        photo.user = request.user
        photo.save()
        add_photo_form.save_m2m()

        return redirect('index')

    context = {
        'form': add_photo_form
    }

    return render(request, 'photos/photo-add-page.html', context)


def details_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    likes = photo.like_set.all()
    comments = photo.comment_set.all()
    comment_form = CommentForm()
    photo_is_liked_by_user = likes.filter(user=request.user)

    context = {
        'photo': photo,
        'photo_likes': likes,
        'photo_comments': comments,
        'photo_likes_count': likes.count(),
        'form': comment_form,
        'user_is_owner': request.user == photo.user,
        'photo_is_liked_by_user': photo_is_liked_by_user
    }

    return render(request, 'photos/photo-details-page.html', context)


def edit_photo(request, pk):
    photo = Photo.objects.filter(pk=pk)\
        .get()

    if request.method == 'GET':
        edit_photo_form = EditPhotoForm(instance=photo)
    else:
        edit_photo_form = EditPhotoForm(request.POST, instance=photo)
        if edit_photo_form.is_valid():
            edit_photo_form.save()
            return redirect('details photo', pk=pk)

    context = {
        'form': edit_photo_form,
        'pk': pk
    }

    return render(request, 'photos/photo-edit-page.html', context)


def delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk)\
        .get()
    photo.like_set.all().delete()
    photo.comment_set.all().delete()
    photo.delete()

    return redirect('index')
