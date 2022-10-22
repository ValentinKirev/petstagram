from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.core.photo_utils import apply_likes_count, apply_user_liked_photo
from petstagram.photos.models import Photo


def index(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm()

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['pet_name']
            all_photos = all_photos.filter(tagged_pets__name__icontains=search_pattern)

    all_photos = [apply_likes_count(photo) for photo in all_photos]
    all_photos = [apply_user_liked_photo(photo) for photo in all_photos]

    context = {
        'photos': all_photos,
        'comment_form': comment_form,
        'search_form': search_form
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


def add_comment_functionality(request, photo_id):
    if request.method == "POST":
        photo = Photo.objects.filter(id=photo_id)\
            .get()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment_form.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
