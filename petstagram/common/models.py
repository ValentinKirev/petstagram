from django.contrib.auth import get_user_model
from django.db import models

from petstagram.core.model_mixins import StrFromFieldMixin
from petstagram.photos.models import Photo

UserModel = get_user_model()


class Comment(StrFromFieldMixin, models.Model):
    str_fields = ('text', 'date_time_of_publication', 'to_photo')

    class Meta:
        ordering = ["-date_time_of_publication"]

    COMMENT_TEXT_MAX_LENGTH = 300

    text = models.TextField(
        max_length=300,
        null=False,
        blank=False
    )

    date_time_of_publication = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True
    )

    to_photo = models.ForeignKey(
        to=Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )


class Like(models.Model):
    str_fields = ('to_photo', )

    to_photo = models.ForeignKey(
        to=Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )
