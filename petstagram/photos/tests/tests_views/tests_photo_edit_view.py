from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy

from petstagram.photos.forms import EditPhotoForm
from petstagram.photos.models import Photo
from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.settings import BASE_DIR


class PhotoEditViewTests(TestCase):
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

    user_data_2 = {
        'username': 'test_user2',
        'password': 'test1234',
        'first_name': 'Ivan',
        'last_name': 'Kolev',
        'email': 'Test2@abv.bg',
        'profile_picture': 'https://i.pinimg.com/originals/25/78/61/25786134576ce0344893b33a051160b1.jpg',
        'gender': 'Male'
    }

    new_photo = SimpleUploadedFile(name='test_image.jpg',
                                   content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                   .read(), content_type='image/jpeg')

    def tearDown(self):
        delete_test_image()

    def test__get_photo_edit_view__should_render_correct_template_when_user_is_owner(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        response = self.client.get(reverse_lazy('edit photo', kwargs={'pk': photo.id}))

        self.assertTemplateUsed(response, 'photos/photo-edit-page.html')

    def test__get_photo_edit_view__should_redirect_to_index_page_when_user_is_not_owner(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        user2 = self.UserModel.objects.create_user(**self.user_data_2)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=user2
        )

        response = self.client.get(reverse_lazy('edit photo', kwargs={'pk': photo.id}))

        self.assertRedirects(response, reverse_lazy('index'))
        self.assertEqual(302, response.status_code)

    def test__get_photo_edit_view__should_return_correct_form_in_context(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        response = self.client.get(reverse_lazy('edit photo', kwargs={'pk': photo.id}))

        self.assertTrue(isinstance(response.context['form'], EditPhotoForm))

    def test__post_photo_edit_view__should_redict_to_photo_details_page_after_success(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        data = photo.__dict__
        response = self.client.post(reverse_lazy('edit photo', kwargs={'pk': photo.id}), data=data)

        self.assertRedirects(response, reverse_lazy('details photo', kwargs={'pk': photo.id}))
        self.assertEqual(302, response.status_code)

    def test__post_photo_edit_view__with_correct_data__should_edit_post(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        old_location = photo.location

        self.assertEqual(old_location, photo.location)

        data = {
            'description': 'Some description',
            'location': 'Plovdiv, Bulgaria',
        }

        response = self.client.post(reverse_lazy('edit photo', kwargs={'pk': photo.id}), data=data)
        photo.refresh_from_db()

        self.assertEqual(302, response.status_code)
        self.assertNotEqual(old_location, photo.location)

    def test__post_photo_edit_view__with_incorrect_data__should_not_edit_post_and_return_status_200(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        old_location = photo.location

        self.assertEqual(old_location, photo.location)

        data = {
            'description': 'Some description',
            'location': 'Plovdiv, Bulgaria but this became invalid data beacuse location is longer than 30 characters',
        }

        response = self.client.post(reverse_lazy('edit photo', kwargs={'pk': photo.id}), data=data)
        photo.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertEqual(old_location, photo.location)

    def test__post_photo_edit_view__without_data__should_edit_post_and_redirect_to_photo_details_page(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        photo = Photo.objects.create(
            photo=self.new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        old_location = photo.location

        self.assertEqual(old_location, photo.location)

        response = self.client.post(reverse_lazy('edit photo', kwargs={'pk': photo.id}), data={})
        photo.refresh_from_db()

        self.assertEqual(302, response.status_code)
        self.assertIsNone(photo.location)
