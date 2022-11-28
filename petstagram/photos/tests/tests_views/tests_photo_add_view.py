from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from petstagram.photos.forms import CreatePhotoForm
from petstagram.photos.models import Photo
from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.settings import BASE_DIR


class PhotoAddViewTests(TestCase):
    UserModel = get_user_model()
    user_data = {
        'username': 'test_user',
        'password': 'test1234',
        'first_name': 'Ivan',
        'last_name': 'Kolev',
        'email': 'Test@abv.bg',
        'profile_picture': 'https://i.pinimg.com/originals/25/78/61/25786134576ce0344893b33a051160b1.jpg',
        'gender': 'Male'
    }

    def tearDown(self):
        delete_test_image()

    def test__get_photo_add_view__should_render_correct_template_when_user_is_logged(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        response = self.client.get(reverse_lazy('add photo'))

        self.assertTemplateUsed(response, 'photos/photo-add-page.html')

    def test__get_photo_add_view__should_redirect_to_login_page_when_user_is_not_logged(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)

        response = self.client.get(reverse_lazy('add photo'))

        self.assertRedirects(response, reverse_lazy('login user') + '?next=/photos/add/')
        self.assertEqual(302, response.status_code)

    def test__get_photo_add_view__should_return_correct_form_in_context_with_logged_user(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        response = self.client.get(reverse_lazy('add photo'))

        self.assertTrue(isinstance(response.context['form'], CreatePhotoForm))

    def test__post_photo_add_view__should_redict_to_index_after_success(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = open(BASE_DIR / 'media/test_images/image.jpg', 'rb')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'tagged_pets': []
        }

        response = self.client.post(reverse_lazy('add photo'), data=data)

        self.assertRedirects(response, reverse_lazy('index'))
        self.assertEqual(302, response.status_code)

    def test__post_photo_add_view__with_correct_data__should_create_post(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = open(BASE_DIR / 'media/test_images/image.jpg', 'rb')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'tagged_pets': []
        }

        response = self.client.post(reverse_lazy('add photo'), data=data)
        created_photo = Photo.objects.last()

        self.assertEqual(302, response.status_code)
        self.assertEqual('Plovdiv', created_photo.location)
        self.assertIsNotNone(created_photo.pk)

    def test__post_photo_add_view__with_incorrect_data__should_not_create_post_and_return_status_200(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = open(BASE_DIR / 'media/test_images/image.jpg', 'rb')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv but this is not a valid location because max_length is greater than 30',
            'tagged_pets': []
        }

        response = self.client.post(reverse_lazy('add photo'), data=data)

        created_photo = Photo.objects.last()

        self.assertEqual(200, response.status_code)
        self.assertIsNone(created_photo)

    def test__post_add_photo_view__with_missing_data__should_not_create_post_and_return_status_200(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        data = {
            'description': 'Some description',
            'location': 'Plovdiv but this is not a valid location because max_length is greater than 30',
            'tagged_pets': []
        }

        response = self.client.post(reverse_lazy('add photo'), data=data)

        created_photo = Photo.objects.last()

        self.assertEqual(200, response.status_code)
        self.assertIsNone(created_photo)

    def test__post_photo_add_view__without_data__should_not_create_post_and_return_status_200(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        response = self.client.post(reverse_lazy('add photo'), data={})

        created_photo = Photo.objects.last()

        self.assertEqual(200, response.status_code)
        self.assertIsNone(created_photo)
