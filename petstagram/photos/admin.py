from django.contrib import admin

from petstagram.photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_publication', 'description', 'get_all_tagged_pets')

    @staticmethod
    def get_all_tagged_pets(obj):
        all_tagged_pets = obj.tagged_pets.all()

        return f"{', '.join([pet.name for pet in all_tagged_pets])}"
