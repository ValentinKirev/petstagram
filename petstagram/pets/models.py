from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class Pet(models.Model):
    NAME_MAX_LENGTH = 30

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        null=False,
        blank=False
    )

    personal_photo = models.URLField(
        null=False,
        blank=False
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.id}")

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
