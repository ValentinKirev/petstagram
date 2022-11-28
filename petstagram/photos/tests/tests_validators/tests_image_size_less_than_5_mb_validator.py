from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from petstagram.photos.tests.tests_utils import delete_test_image
from petstagram.photos.validators import validate_image_size_less_than_5mb
from petstagram.settings import BASE_DIR


class ImageSizeLessThan5MbValidator(TestCase):
    def tearDown(self):
        delete_test_image()

    def test_image_size_less_than_5mb_validator__with_valid_image_size__expect_to_do_nothing(self):
        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        validate_image_size_less_than_5mb(new_photo)

        self.assertTrue(True)

    def test_image_size_less_than_5mb_validator__with_invalid_image_size__expect_to_raise(self):
        new_photo = SimpleUploadedFile(name='test_image.jpg',
                                       content=open(BASE_DIR / 'media/test_images/large_image.jpg', 'rb')
                                       .read(), content_type='image/jpeg')

        with self.assertRaises(ValidationError) as ex:
            validate_image_size_less_than_5mb(new_photo)

        self.assertIsNotNone(ex.exception)
        self.assertEqual(ex.exception.args[0], 'The maximum file size that can be uploaded is 5MB')