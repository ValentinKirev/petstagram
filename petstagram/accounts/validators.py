from django.core.exceptions import ValidationError


def validate_only_alphabetical_letters(value):
    for character in value:
        if not character.isalpha():
            raise ValidationError(f"Name can only contain letters.")
