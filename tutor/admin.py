from django.contrib import admin
from .models import TemporaryTutorRegistration, Tutor, AcademicQualification, TutorCourse, TutorialLocation, TutorialSession
# Register your models here.
admin.site.register(TemporaryTutorRegistration)
admin.site.register(Tutor)
admin.site.register(AcademicQualification)
admin.site.register(TutorCourse)
admin.site.register(TutorialLocation)
admin.site.register(TutorialSession)
