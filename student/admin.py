from django.contrib import admin
from .models import TemporaryStudentRegistration, Student
# Register your models here.
admin.site.register(TemporaryStudentRegistration)
admin.site.register(Student)
