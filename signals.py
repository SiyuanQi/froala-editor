import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

from aliyun_oss2_storage.backends import AliyunBaseStorage
from .models import FroalaImage


@receiver(pre_delete, sender=FroalaImage)
def delete_froala_image(sender, instance, using, **kwargs):
    print('signal triggered!')
    if settings.ENVIRONMENT == 'local':
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.image.name))
    elif settings.ENVIRONMENT == 'production':
        storage = AliyunBaseStorage()
        storage.delete(os.path.join(settings.MEDIA_ROOT, instance.image.name))