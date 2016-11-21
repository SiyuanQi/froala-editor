# -*- coding: utf-8 -*-
import os
import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


def image_upload_to(instance, filename):
    path = os.path.join(getattr(settings, 'FROALA_IMAGE_UPLOAD_PATH', 'uploads/froala_editor/images/'), uuid.uuid4().hex)
    return path


def audio_upload_to(instance, filename):
    path = os.path.join(getattr(settings, 'FROALA_FILE_UPLOAD_PATH', 'uploads/froala_editor/files/'), uuid.uuid4().hex)
    return path


def sheet_upload_to(instance, filename):
    path = os.path.join(getattr(settings, 'FROALA_FILE_UPLOAD_PATH', 'uploads/froala_editor/files/'), uuid.uuid4().hex)
    return path


def video_upload_to(instance, filename):
    path = os.path.join(getattr(settings, 'FROALA_FILE_UPLOAD_PATH', 'uploads/froala_editor/files/'), uuid.uuid4().hex)
    return path


# generic foreigen key:
# https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/
class FroalaMedia(models.Model):
    id = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)  # Allow to be saved without this foreign key
    object_id = models.PositiveIntegerField(null=True, blank=True)
    filename = models.CharField(max_length=250, default=None)
    content_object = GenericForeignKey('content_type', 'object_id')

    # user_profile = models.ForeignKey(account_models.Profile, default=0)

    class Meta:
        abstract = True


class FroalaSheet(FroalaMedia):
    sheet = models.FileField(upload_to=sheet_upload_to, verbose_name='乐谱')

    class Meta:
        db_table = 'froala_sheet'

    def __str__(self):
        return 'FroalaSheet: {}'.format(str(self.sheet))


class FroalaImageManager(models.Manager):
    def delete_from_src(self, src):
        if src.startswith(settings.MEDIA_URL):
            print(src[len(settings.MEDIA_URL):])
            src = src[len(settings.MEDIA_URL):]
        self.filter(image=src).delete()

    def save_content_object(self, src, object):
        if src.startswith(settings.MEDIA_URL):
            print(src[len(settings.MEDIA_URL):])
            src = src[len(settings.MEDIA_URL):]
        images = self.filter(image=src)
        for image in images:
            image.content_object = object
            image.save()


class FroalaImage(FroalaMedia):
    image = models.ImageField(upload_to=image_upload_to, verbose_name='图片')
    objects = FroalaImageManager()

    class Meta:
        db_table = 'froala_images'

    def __str__(self):
        return 'FroalaImage: {}'.format(str(self.image))


class FroalaAudio(FroalaMedia):
    audio = models.FileField(upload_to=audio_upload_to, verbose_name='音频')

    class Meta:
        db_table = 'froala_audio'

    def __str__(self):
        return 'FroalaAudio: {}'.format(str(self.image))

    def as_json(self):
        return dict(id=self.id, url=str(self.audio), name=self.filename)


class FroalaVideo(FroalaMedia):
    video = models.FileField(upload_to=video_upload_to, verbose_name='音频')

    class Meta:
        db_table = 'froala_video'

    def __str__(self):
        return 'FroalaVideo: {}'.format(str(self.video))

    def as_json(self):
        return dict(id=self.id, url=str(self.video), name=self.filename)
