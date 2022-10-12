from django.shortcuts import render

from petstagram.photos.models import Photo


def add_photo(request):
    return render(request, 'photos/photo-add-page.html')


def details_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    likes = photo.like_set.all()
    comments = photo.comment_set.all()

    context = {
        'photo': photo,
        'photo_likes': likes,
        'photo_comments': comments,
        'photo_likes_count': likes.count()
    }

    return render(request, 'photos/photo-details-page.html', context)


def edit_photo(request, pk):
    return render(request, 'photos/photo-edit-page.html')
