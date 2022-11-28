from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from petstagram.pets.models import Pet
from petstagram.photos.forms import EditPhotoForm
from petstagram.photos.tests.tests_utils import delete_test_image


class PhotoEditFormTests(TestCase):
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

    def test__photo_edit_form_is_valid__with_valid_data__expect_true(self):
        self.user.save()
        tagged_pets = set()

        self.pet1.save()
        self.pet2.save()

        tagged_pets.add(self.pet1)
        tagged_pets.add(self.pet2)

        data = {
            'description': 'Some description',
            'location': 'Plovdiv',
            'tagged_pets': tagged_pets
        }

        form = EditPhotoForm(data)
        self.assertTrue(form.is_valid())

    def test__photo_edit_form_is_valid__with_invalid_data__expect_false(self):
        self.user.save()
        tagged_pets = set()

        self.pet1.save()
        self.pet2.save()

        tagged_pets.add(self.pet1)
        tagged_pets.add(self.pet2)

        data = {
            'description': 'Some description',
            'location': 'Plovdiv, Bulgaria, More text to became invalid max length',
        }

        form = EditPhotoForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))

    def test__photo_edit_form_is_valid_without_data__expect_true_because_there_is_no_required_fields_in_form(self):
        data = {}

        form = EditPhotoForm(data)

        self.assertTrue(form.is_valid())
        self.assertEqual(0, len(form.errors))

    def test__photo_create_form_fields__expect_to_have_correct_fields(self):
        form = EditPhotoForm()

        form_fields = [name for name, field in form.fields.items()]

        self.assertTrue('description' in form_fields)
        self.assertTrue('location' in form_fields)
        self.assertTrue('tagged_pets' in form_fields)
