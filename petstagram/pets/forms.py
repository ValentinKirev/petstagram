from django import forms

from petstagram.pets.models import Pet


class BasePetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'date_of_birth', 'personal_photo']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Pet name'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'mm/dd/yyyy',
                    'type': 'date',
                }
            ),
            'personal_photo': forms.TextInput(
                attrs={
                    'placeholder': 'Link to Image'
                }
            )
        }
        labels = {
            'name': 'Pet Name',
            'date_of_birth': 'Date of Birth',
            'personal_photo': 'Link to Image'
        }


class CreatePetForm(BasePetForm):
    pass


class EditPetForm(BasePetForm):
    pass


class DeletePetForm(BasePetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'
