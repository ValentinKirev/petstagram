# Generated by Django 4.1.2 on 2022-10-12 06:22

from django.db import migrations, models
import petstagram.photos.validators


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='media/pet_photos/', validators=[petstagram.photos.validators.validate_image_sile_less_than_5mb]),
        ),
    ]
