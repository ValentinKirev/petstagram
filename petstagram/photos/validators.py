from django.core.exceptions import ValidationError


def validate_image_sile_less_than_5mb(image_object):
    if image_object.size > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")