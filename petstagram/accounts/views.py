from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from petstagram.accounts.forms import UserCreateForm, LoginForm, UserEditForm, UserDeleteForm
from petstagram.core.view_mixins import UserOwnerMixin

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'accounts/register-page.html'
    model = UserModel
    form_class = UserCreateForm
    success_url = reverse_lazy('login user')


class SignInView(LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginForm


class SignOutView(LogoutView):
    pass


class UserEditView(UserOwnerMixin, UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    form_class = UserEditForm

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.object.pk
        })


class UserDetailsView(DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_photos = self.object.photo_set.prefetch_related('like_set')
        photos_for_pagination = self.object.photo_set.all()
        paginator = Paginator(photos_for_pagination, 2)
        page_number = self.request.GET.get('page') or 1
        page_object = paginator.get_page(page_number)

        context['photos_count'] = all_photos.count()
        context['pets_count'] = self.object.pet_set.count()
        context['likes_count'] = sum(photo.like_set.count() for photo in all_photos)
        context['page_object'] = page_object
        return context


class UserDeleteView(UserOwnerMixin, DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    form_class = UserDeleteForm
    success_url = reverse_lazy('index')

    def form_valid(self, form, success_url=success_url):
        photos = self.object.photo_set.all()

        for photo in photos:
            photo.comment_set.all().delete()
            photo.like_set.all().delete()

        self.object.like_set.all().delete()
        self.object.pet_set.all().delete()
        photos.delete()
        self.object.comment_set.all().delete()
        self.object.delete()

        return HttpResponseRedirect(success_url)
