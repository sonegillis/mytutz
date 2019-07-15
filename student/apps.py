from django.apps import AppConfig


class StudentConfig(AppConfig):
    name = 'student'
    label = 'student'

    def ready(self):
        import name.signals
