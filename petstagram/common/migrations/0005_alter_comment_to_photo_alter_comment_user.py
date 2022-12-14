# Generated by Django 4.1.2 on 2022-11-11 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0006_alter_photo_user'),
        ('common', '0004_comment_user_like_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='to_photo',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='photos.photo'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
