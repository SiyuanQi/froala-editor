from django.apps import AppConfig

class FroalaEditorConfig(AppConfig):
    name = 'froala_editor'

    def ready(self):
        import froala_editor.signals