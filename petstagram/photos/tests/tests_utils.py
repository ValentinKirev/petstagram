import os

from petstagram.settings import BASE_DIR


def delete_test_image():
    images_path = os.path.join(BASE_DIR, 'media/images')
    files = [i for i in os.listdir(images_path)
             if os.path.isfile(os.path.join(images_path, i))
             and i.startswith('test_image')]

    for file in files:
        os.remove(os.path.join(images_path, file))
