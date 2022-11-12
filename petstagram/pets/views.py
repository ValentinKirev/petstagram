from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.core.view_mixins import UserOwnerMixin
from petstagram.pets.forms import CreatePetForm, EditPetForm, DeletePetForm
from petstagram.pets.models import Pet

UserModel = get_user_model()


class PetAddView(CreateView):
    template_name = 'pets/pet-add-page.html'
    form_class = CreatePetForm
    model = Pet

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        pet.save()
        return redirect('details user', self.request.user.pk)


class PetDetailView(DetailView):
    template_name = 'pets/pet-details-page.html'
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_photos = self.object.photo_set.all()

        context['pet_photos'] = pet_photos
        context['pet_photos_count'] = pet_photos.count()
        context['comment_form'] = CommentForm()
        context['owner'] = self.object.user
        return context


class PetEditView(UserOwnerMixin, UpdateView):
    template_name = 'pets/pet-edit-page.html'
    model = Pet
    form_class = EditPetForm

    def get_success_url(self):
        return reverse_lazy('details pet', kwargs={
            'username': self.object.user.username,
            'slug': self.object.slug
        })


class PetDeleteView(UserOwnerMixin, DeleteView):
    template_name = 'pets/pet-delete-page.html'
    model = Pet
    form_class = DeletePetForm

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.request.user.id
        })

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_object())
        context = {
            'form': form,
            'slug': kwargs['slug']
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('details user', request.user.id)
