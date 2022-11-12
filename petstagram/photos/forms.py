from django import forms

from petstagram.photos.models import Photo


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['user']
        labels = {
            'photo': 'Photo file',
            'tagged_pets': 'Tag Pets'
        }


class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['photo', 'user']
        labels = {
            'tagged_pets': 'Tag Pets'
        }
