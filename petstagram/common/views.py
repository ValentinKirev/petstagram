from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.models import Like
from petstagram.core.photo_utils import apply_likes_count, apply_user_liked_photo
from petstagram.photos.models import Photo


def index(request):
    all_photos = Photo.objects.all()

    all_photos = [apply_likes_count(photo) for photo in all_photos]
    all_photos = [apply_user_liked_photo(photo) for photo in all_photos]

    context = {
        'photos': all_photos,
    }

    return render(request, 'common/home-page.html', context)


def like_functionality(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    liked_object = Like.objects.filter(to_photo_id=photo_id)\
        .first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo=photo)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


def share_functionality(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('details photo', pk=photo_id))

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
