from django.shortcuts import render, redirect, resolve_url
from django.views.generic import TemplateView
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


class IndexView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['photos'] = Photo.objects.all()
        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm()

        photos_liked_by_current_user = []
        if self.request.user.is_authenticated:
            photos_liked_by_current_user = [like.to_photo_id for like in self.request.user.like_set.all()]

        context['photos_liked_by_current_user'] = photos_liked_by_current_user

        return context

    def post(self, request, *args, **kwargs):
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['pet_name']

            context = self.get_context_data()
            context['photos'] = context['photos'].filter(tagged_pets__name__icontains=search_pattern)

            return render(request, self.template_name, context)


def like_functionality(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    liked_object = Like.objects.filter(to_photo_id=photo_id, user=request.user)\
        .first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo=photo, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


def share_functionality(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('details photo', pk=photo_id))

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


def add_comment_functionality(request, photo_id):
    if request.method == "POST":
        photo = Photo.objects.filter(id=photo_id) \
            .get()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment_form.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
