import json

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms import widgets, Media
from django.utils.safestring import mark_safe

from . import PLUGINS, PLUGINS_WITH_CSS


class FroalaEditor(widgets.Textarea):
    def __init__(self, *args, **kwargs):
        self.options = kwargs.pop('options', {})
        self.plugins = kwargs.pop('plugins', getattr(settings, 'FROALA_EDITOR_PLUGINS', PLUGINS))
        self.theme = kwargs.pop('theme', getattr(settings, 'FROALA_EDITOR_THEME', None))
        self.include_jquery = kwargs.pop('include_jquery', getattr(settings, 'FROALA_INCLUDE_JQUERY', True))
        self.image_upload = kwargs.pop('image_upload', True)
        self.file_upload = kwargs.pop('file_upload', True)
        self.language = (getattr(settings, 'FROALA_EDITOR_OPTIONS', {})).get('language', '')
        super(FroalaEditor, self).__init__(*args, **kwargs)

    def get_options(self):

        default_options = {
            'inlineMode': False,
        }

        try:
            image_upload_url = reverse('froala_editor_image_upload')
            default_options['imageUploadURL'] = image_upload_url
            default_options.update([('imageUploadParams', {'csrfmiddlewaretoken': 'csrftokenplaceholder'})])
        except NoReverseMatch:
            default_options['imageUpload'] = False

        try:
            file_upload_url = reverse('froala_editor_file_upload')
            default_options['fileUploadURL'] = file_upload_url
            default_options.update([('fileUploadParams', {'csrfmiddlewaretoken': 'csrftokenplaceholder'})])
        except NoReverseMatch:
            default_options['fileUpload'] = False

        settings_options = getattr(settings, 'FROALA_EDITOR_OPTIONS', {})
        # options = dict(default_options.items() + settings_options.items() + self.options.items())
        options = dict(default_options.items()).copy()
        options.update(settings_options.items())
        options.update(self.options.items())

        if self.theme:
            options['theme'] = self.theme

        json_options = json.dumps(options)
        json_options = json_options.replace('"csrftokenplaceholder"', 'getCookie("csrftoken")')
        return json_options

    def get_events(self):
        # This events calls a url from server when a image is deleted from the editor.
        # The server then deletes the image uploaded.
        image_removed = """
        .on('froalaEditor.image.removed', function (e, editor, $img) {
            $.ajax({
                // Request method.
                method: "GET",

                // Request URL.
                url: "/froala_editor/image/delete/",

                // Request params.
                data: {
                    src: $img.attr('src')
                }
            })
            .done(function (data) {
                console.log(data);
                console.log('image was deleted');
            })
            .fail(function () {
                console.log('image delete problem');
            })
        })
        """
        events = image_removed
        return events

    def render(self, name, value, attrs=None):
        attrs['froala'] = True
        html = super(FroalaEditor, self).render(name, value, attrs)
        # el_id = self.build_attrs(attrs).get('id')
        # eigenTunes
        el_id = 'div#question_form_content p textarea, div#post_edit_form_content p textarea'
        html += self.trigger_froala(el_id, self.get_options(), self.get_events())
        return mark_safe(html)

    def trigger_froala(self, el_id, options, events):

        # eigenTunes
        str = """
        <script>
            $(function(){
                $('%s').froalaEditor(%s)%s
            });
        </script>""" % (el_id, options, events)
        return str

    def _media(self):
        css = {
            'all': ('eigenTunes/css/font-awesome-4.6.3/css/font-awesome.min.css',
                    'froala_editor/css/froala_editor.min.css', 'froala_editor/css/froala_style.min.css',
                    'froala_editor/css/froala-django.css')
        }
        js = ('froala_editor/js/froala_editor.min.js', 'froala_editor/js/froala-django.js',)

        if self.include_jquery:
            # Since eigenTunes superbase page includes jquery library, we do not need to load it twice
            pass
            # js = ('https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js',) + js

        if self.theme:
            css['all'] += ('froala_editor/css/themes/' + self.theme + '.css',)

        if self.language:
            js += ('froala_editor/js/languages/' + self.language + '.js',)

        for plugin in self.plugins:
            js += ('froala_editor/js/plugins/' + plugin + '.min.js',)
            if plugin in PLUGINS_WITH_CSS:
                css['all'] += ('froala_editor/css/plugins/' + plugin + '.min.css',)

        return Media(css=css, js=js)

    media = property(_media)
