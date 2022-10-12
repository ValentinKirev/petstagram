from django.db import models

from petstagram.photos.models import Photo


class Comment(models.Model):
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


class Like(models.Model):

    to_photo = models.ForeignKey(
        to=Photo,
        on_delete=models.RESTRICT,
        null=False,
        blank=True
    )
