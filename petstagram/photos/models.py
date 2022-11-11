from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.core.model_mixins import StrFromFieldMixin
from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_image_sile_less_than_5mb

UserModel = get_user_model()


class Photo(StrFromFieldMixin, models.Model):
    str_fields = ('id', 'photo', 'description')

    DESCRIPTION_MAX_LENGTH = 300
    LOCATION_MAX_LENGTH = 30

    photo = models.ImageField(
        upload_to='images',
        validators=(validate_image_sile_less_than_5mb,),
        null=False,
        blank=False,
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        validators=(MinLengthValidator(10), ),
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        null=True,
        blank=True
    )

    date_of_publication = models.DateField(
        auto_now=True,
        null=False,
        blank=True
    )

    tagged_pets = models.ManyToManyField(
        to=Pet,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )
