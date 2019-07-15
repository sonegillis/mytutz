"""mytutz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from mainapp.views import homepage, pre_registration, complete_registration, verify_email, user_login, user_logout, \
                            get_faculty_options, get_department_options

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="home"),
    path('pre-registration/', pre_registration, name="pre-registration"),
    path('complete-registration/', complete_registration, name="complete-registration"),
    path('faculty-options/', get_faculty_options, name="get-faculty-options"),
    path('department-options/', get_department_options, name="get-department-options"),
    path('verify-email/', verify_email, name="verify-email"),
    path('student/', include(('student.urls', 'student'), namespace="student")),
    path('tutor/', include(('tutor.urls', 'tutor'), namespace="tutor")),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
