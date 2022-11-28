
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy

from petstagram.common.models import Like, Comment
from petstagram.photos.models import Photo
from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.settings import BASE_DIR


class PhotoDeleteViewTests(TestCase):
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

    def tearDown(self):
        delete_test_image()

    def test__get_photo_delete_view__should_redirect_to_index_without_delete_photo_when_user_is_not_owner(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        user2 = self.UserModel.objects.create_user(**self.user_data_2)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        photo = Photo.objects.create(
            photo=new_photo,
            description='Some description',
            location='Plovdiv',
            user=user2
        )

        response = self.client.get(reverse_lazy('delete photo', kwargs={'pk': photo.id}))

        self.assertRedirects(response, reverse_lazy('index'))
        self.assertEqual(302, response.status_code)
        self.assertIsNotNone(photo.id)

    def test__get_photo_delete_view__should_redirect_to_index_and_delete_photo_comments_and_likes_when_user_is_owner(self):
        self.user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        photo = Photo.objects.create(
            photo=new_photo,
            description='Some description',
            location='Plovdiv',
            user=self.user
        )

        Like.objects.create(
            to_photo=photo,
            user=self.user
        )

        Comment.objects.create(
            text='Some comment',
            to_photo=photo,
            user=self.user
        )

        self.assertEqual(1, Photo.objects.count())
        self.assertEqual(1, Like.objects.count())
        self.assertEqual(1, Comment.objects.count())

        response = self.client.get(reverse_lazy('delete photo', kwargs={'pk': photo.pk}))

        self.assertRedirects(response, reverse_lazy('index'))
        self.assertEqual(302, response.status_code)

        with self.assertRaises(Photo.DoesNotExist) as ex:
            Photo.objects.get(id=photo.id)

        self.assertIsNotNone(ex.exception)
        self.assertEqual(0, Photo.objects.count())
        self.assertEqual(0, Like.objects.count())
        self.assertEqual(0, Comment.objects.count())
