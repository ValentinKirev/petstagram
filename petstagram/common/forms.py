from django import forms
from django.forms import TextInput

from petstagram.common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Add comment...'
                }
            )
        }


class SearchForm(forms.Form):
    pet_name = forms.CharField(
        widget=TextInput(
            attrs={
                'placeholder': 'Search by pet name...'
            }
        )
    )
