from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from petstagram.pets.models import Pet
from petstagram.photos.forms import CreatePhotoForm
from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.settings import BASE_DIR


class PhotoCreateFormTests(TestCase):
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

    pet1 = Pet(
        name='test_pet',
        personal_photo='https://some_url.com',
        date_of_birth=datetime.now(),
        user=user
    )

    pet2 = Pet(
        name='test_pet2',
        personal_photo='https://some_url2.com',
        date_of_birth=datetime.now(),
        user=user
    )

    def tearDown(self):
        delete_test_image()

    def test__photo_create_form_is_valid__with_valid_data__expect_true(self):
        self.user.save()
        tagged_pets = set()

        self.pet1.save()
        self.pet2.save()

        tagged_pets.add(self.pet1)
        tagged_pets.add(self.pet2)

        new_photo = open(BASE_DIR / 'media/test_images/image.jpg', 'rb')

        data = {
            'description': 'Some description',
            'location': 'Plovdiv',
            'tagged_pets': tagged_pets
        }

        files_data = {
            'photo': SimpleUploadedFile(new_photo.name, new_photo.read())
        }

        form = CreatePhotoForm(data, files_data)
        self.assertTrue(form.is_valid())

    def test__photo_create_form_is_valid__with_invalid_data__expect_false(self):
        self.user.save()
        tagged_pets = set()

        self.pet1.save()
        self.pet2.save()

        tagged_pets.add(self.pet1)
        tagged_pets.add(self.pet2)

        new_photo = open(BASE_DIR / 'media/test_images/image.jpg', 'rb')

        data = {
            'description': 'Some description',
            'location': 'Plovdiv, Bulgaria, More text to became invalid max length',
        }

        files_data = {
            'photo': SimpleUploadedFile(new_photo.name, new_photo.read())
        }

        form = CreatePhotoForm(data, files_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))

    def test__photo_create_form_is_valid_without_data__expect_false(self):
        data = {}

        form = CreatePhotoForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))

    def test__photo_create_form_is_valid_with_missing_data__expect_false(self):
        self.user.save()
        tagged_pets = set()

        self.pet1.save()
        self.pet2.save()

        tagged_pets.add(self.pet1)
        tagged_pets.add(self.pet2)

        data = {
            'description': 'Some description',
            'location': 'Plovdiv',
        }

        files_data = {}

        form = CreatePhotoForm(data, files_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))

    def test__photo_create_form_fields__expect_to_have_correct_fields(self):
        form = CreatePhotoForm()

        form_fields = [name for name, field in form.fields.items()]

        self.assertTrue('photo' in form_fields)
        self.assertTrue('description' in form_fields)
        self.assertTrue('location' in form_fields)
        self.assertTrue('tagged_pets' in form_fields)
