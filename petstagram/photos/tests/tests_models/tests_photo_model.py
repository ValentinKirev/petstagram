from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from petstagram.photos.models import Photo
from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.settings import BASE_DIR


class PhotoModelTests(TestCase):
    UserModel = get_user_model()
    user = UserModel(
        username='test_user',
        password='test1234',
        first_name='Ivan',
        last_name='Kolev',
        email='Test@abv.bg',
        profile_picture='https://i.pinimg.com/originals/25/78/61/25786134576ce0344893b33a051160b1.jpg',
        gender='Male'
    )

    def tearDown(self):
        delete_test_image()

    def test_photo_model_save__with_invalid_data__expect_to_create_it(self):
        new_photo = SimpleUploadedFile(name='test_image.jpg', content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        self.user.full_clean()
        self.user.save()

        photo = Photo(
            photo=new_photo,
            description='Some description',
            location='Plovdiv',
            date_of_publication=datetime.now(),
            user=self.user
        )

        photo.full_clean()
        photo.save()

        self.assertIsNotNone(photo.pk)

    def test_photo_model_save__with_invalid_data__expect_to_raise(self):
        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/large_image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        self.user.full_clean()
        self.user.save()

        photo = Photo(
            photo=new_photo,
            description='Some description',
            location='Plovdiv',
            date_of_publication=datetime.now(),
            user=self.user
        )

        with self.assertRaises(ValidationError) as ex:
            photo.full_clean()

        self.assertIsNotNone(ex.exception)
        self.assertEqual(ex.exception.args[0]['photo'][0].message, 'The maximum file size that can be uploaded is 5MB')

    def test_photo_model_save__without_data__expect_to_raise(self):
        photo = Photo()

        with self.assertRaises(ValidationError) as ex:
            photo.full_clean()

        self.assertIsNotNone(ex.exception)
