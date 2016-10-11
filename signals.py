import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

from aliyun_oss2_storage.backends import AliyunBaseStorage
from .models import FroalaImage


@receiver(pre_delete, sender=FroalaImage)
def delete_froala_image(sender, instance, using, **kwargs):
    """
    This function is called when an image is removed when editing.
    It deletes the image from the server when the model instance in the database is deleted.
    :param sender: The model class which is sending the signal
    :param instance: The post/reply as the content object which contains the image
    :param using: The database alias being used.
    :param kwargs: extra arguments
    """
    if settings.ENVIRONMENT == 'local':
        # Local development
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.image.name))
    elif settings.ENVIRONMENT == 'production':
        # Server environment
        storage = AliyunBaseStorage()
        storage.delete(os.path.join(settings.MEDIA_ROOT, instance.image.name))