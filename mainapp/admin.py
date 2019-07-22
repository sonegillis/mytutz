from django.contrib import admin
from .models import User, Institution, Faculty, Department, Country, Course
# Register your models here.

admin.site.register(User)
admin.site.register(Institution)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Country)
admin.site.register(Course)