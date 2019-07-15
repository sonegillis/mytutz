from django.contrib import admin
from django.urls import path, include
from .views import home, profile, complete_profile, edit_profile, my_courses, application_status

urlpatterns = [
    path('home/', home, name="home"),
    path('complete-profile/', complete_profile, name="complete-profile"),
    path('edit-profile/', edit_profile, name="edit-profile"),
    path('profile/', profile, name="profile"),
    # path('schedule-a-tutorial/', schedule_a_tutorial, name="schedule-a-tutorial"),
    path('my-courses/', my_courses, name="my-courses"),
    path('application-status/', application_status, name="application-status")
]