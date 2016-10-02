from django.conf.urls import url
from froala_editor import views

urlpatterns = [
    url(r'^image_upload/$', views.image_upload, name='froala_editor_image_upload'),
    url(r'^file_upload/$', views.file_upload, name='froala_editor_file_upload'),

    # File deletion
    url(r'^image/delete/$', views.delete_image, name='froala_delete_image'),
]
