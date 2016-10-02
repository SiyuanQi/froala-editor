import json
# from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect

from .models import FroalaImage


def image_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        allowed_types = ['image/jpeg', 'image/jpg', 'image/pjpeg', 'image/x-png', 'image/png', 'image/gif']
        if not the_file.content_type in allowed_types:
            return HttpResponse(json.dumps({'error': _('You can only upload images.')}),
                                content_type="application/json")
        # Other data on the request.FILES dictionary:
        # filesize = len(file['content'])
        # filetype = file['content-type']
        # eigenTunes
        # upload_to = getattr(settings, 'FROALA_IMAGE_UPLOAD_PATH', 'uploads/froala_editor/images/')
        # path = default_storage.save(os.path.join(upload_to, the_file.name), the_file)
        # link = default_storage.url(path)

        filename = the_file.name
        image = FroalaImage(image=the_file, filename=filename)
        image.save()

        # return JsonResponse({'link': link})
        return HttpResponse(json.dumps({'link': os.path.join(settings.MEDIA_URL, str(image.image))}), content_type="application/json")


def file_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        # eigenTunes
        upload_to = getattr(settings, 'FROALA_FILE_UPLOAD_PATH', 'uploads/froala_editor/files/')
        path = default_storage.save(os.path.join(upload_to, the_file.name), the_file)
        link = default_storage.url(path)
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")


def delete_image(request):
    FroalaImage.objects.delete_from_src(request.GET['src'])

    return HttpResponse("")