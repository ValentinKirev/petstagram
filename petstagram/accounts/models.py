from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.accounts.validators import validate_only_alphabetical_letters


class AppUser(AbstractUser):
    MAX_FIRST_NAME_LENGTH = 30
    MIN_FIRST_NAME_LENGTH = 2
    MAX_LAST_NAME_LENGTH = 30
    MIN_LAST_NAME_LENGTH = 2

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDER_CHOICES = [
        (MALE, MALE),
        (FEMALE, FEMALE),
        (DO_NOT_SHOW, DO_NOT_SHOW)
    ]

    MAX_CHOICES_LENGTH = max(len(value) for (name, value) in GENDER_CHOICES)

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_FIRST_NAME_LENGTH),
            validate_only_alphabetical_letters
        ),
        null=True,
        blank=True
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_LAST_NAME_LENGTH),
            validate_only_alphabetical_letters
        ),
        null=True,
        blank=True
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )

    profile_picture = models.URLField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=MAX_CHOICES_LENGTH,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    def get_user_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.username
