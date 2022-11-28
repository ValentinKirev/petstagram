from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy

from petstagram.common.forms import CommentForm
from petstagram.common.models import Like, Comment
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo
from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.settings import BASE_DIR


class PhotoDetailsViewTests(TestCase):
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

    def test__get_photo_details_view__should_render_correct_template(self):
        user = self.UserModel.objects.create_user(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user
        }

        photo = Photo.objects.create(**data)

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertTemplateUsed(response, 'photos/photo-details-page.html')

    def test__get_photo_details_view__should_return_correct_context_when_logged_user_is_owner(self):
        user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        user2 = self.UserModel.objects.create_user(**self.user_data_2)

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user2
        }

        photo = Photo.objects.create(**data)

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertFalse(response.context['user_is_owner'])

    def test__get_photo_details_view__should_return_correct_context_when_photo_is_liked_by_logged_user(self):
        user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user
        }

        photo = Photo.objects.create(**data)

        like = Like.objects.create(
            to_photo=photo,
            user=user
        )

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertTrue(response.context['photo_is_liked_by_user'])

    def test__get_photo_details_view__should_return_correct_context_when_photo_is_not_liked_by_logged_user(self):
        user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user
        }

        photo = Photo.objects.create(**data)

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertFalse(response.context['photo_is_liked_by_user'])

    def test__get_photo_details_view__should_return_correct_context_when_logged_user_is_not_owner(self):
        user = self.UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user
        }

        photo = Photo.objects.create(**data)

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertTrue(response.context['user_is_owner'])

    def test__get_photo_details_view__should_return_correct_context_with_photo_without_tagged_pets_likes_and_comments(self):
        user = self.UserModel.objects.create_user(**self.user_data)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user
        }

        photo = Photo.objects.create(**data)

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertTrue(isinstance(response.context['form'], CommentForm))
        self.assertEqual([], list(response.context['photo_likes']))
        self.assertEqual([], list(response.context['photo_comments']))
        self.assertEqual(0, response.context['photo_likes_count'])
        self.assertEqual(response.context['photo'], photo)

    def test__get_photo_details_view__should_return_correct_context_with_photo_with_tagged_pets_likes_and_comments(self):
        user = self.UserModel.objects.create_user(**self.user_data)
        user2 = self.UserModel.objects.create_user(**self.user_data_2)

        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        data = {
            'photo': new_photo,
            'description': 'Some description',
            'location': 'Plovdiv',
            'user': user
        }

        photo = Photo.objects.create(**data)
        photo.save()

        like1 = Like.objects.create(
            to_photo=photo,
            user=user
        )

        like2 = Like.objects.create(
            to_photo=photo,
            user=user2
        )

        likes = [like1, like2]

        comment1 = Comment.objects.create(
            text="first comment",
            to_photo=photo,
            user=user
        )

        comment2 = Comment.objects.create(
            text="second comment",
            to_photo=photo,
            user=user2
        )

        comments = [comment2, comment1]

        pet1 = Pet(
            name='Sasho',
            personal_photo='https://some_url.com',
            date_of_birth=datetime.now(),
            user=user
        )

        pet1.save()

        pet2 = Pet(
            name='Gosho',
            personal_photo='https://some_url2.com',
            date_of_birth=datetime.now(),
            user=user2
        )

        pet2.save()

        photo.tagged_pets.add(pet1)
        photo.tagged_pets.add(pet2)
        photo.save()

        response = self.client.get(reverse_lazy('details photo', kwargs={'pk': photo.id}))

        self.assertTrue(isinstance(response.context['form'], CommentForm))
        self.assertListEqual(likes, list(response.context['photo_likes']))
        self.assertListEqual(comments, list(response.context['photo_comments']))
        self.assertEqual(2, response.context['photo_likes_count'])
        self.assertListEqual([pet1, pet2], list(photo.tagged_pets.all()))
        self.assertEqual(response.context['photo'], photo)
