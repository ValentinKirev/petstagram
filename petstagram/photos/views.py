from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.core.view_mixins import UserOwnerMixin
from petstagram.photos.forms import CreatePhotoForm, EditPhotoForm
from petstagram.photos.models import Photo


class PhotoAddView(CreateView):
    template_name = 'photos/photo-add-page.html'
    model = Photo
    form_class = CreatePhotoForm

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        form.save_m2m()
        return redirect('index')


class PhotoDetailsView(DetailView):
    template_name = 'photos/photo-details-page.html'
    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.object
        likes = self.object.like_set.all()

        context['photo_likes'] = likes
        context['photo_comments'] = self.object.comment_set.all()
        context['photo_likes_count'] = likes.count()
        context['user_is_owner'] = self.request.user == photo.user
        context['photo_is_liked_by_user'] = likes.filter(user=self.request.user if self.request.user.is_authenticated else False)
        context['form'] = CommentForm()

        return context


class PhotoEditView(UserOwnerMixin, UpdateView):
    template_name = 'photos/photo-edit-page.html'
    model = Photo
    form_class = EditPhotoForm

    def get_success_url(self):
        return reverse_lazy('details photo', kwargs={
            'pk': self.object.pk
        })


class PhotoDeleteView(UserOwnerMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        photo = Photo.objects.filter(pk=kwargs['pk']).get()
        photo.like_set.all().delete()
        photo.comment_set.all().delete()
        photo.delete()

        return redirect('index')
