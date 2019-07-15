# django related imports
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

# app related imports
from student.models import Student
from mainapp.models import Institution, Faculty, Department, User
from mainapp.views import generate_referral_code, category_check_factory_dectorator

#system related imports 
import math
import random

def profile_completion_redirect(func):
    # use this function as decorator to
    # redirect to complete profile or not based on if the 
    # his student entry has been recorded
    def inner(*args, **kwargs):
        if Student.objects.filter(user=args[0].user).exists():
            httpResponse = func(*args, **kwargs)
            return httpResponse
        else: 
            return HttpResponseRedirect(reverse('student:complete-profile'))
    return inner

@login_required
@category_check_factory_dectorator('student')
@profile_completion_redirect
def home(request):
    # if prompt_profile_completion(request.user):
    #     return HttpResponseRedirect(reverse('student:complete-profile'))
    student = Student.objects.filter(user = request.user)
    context = {
        "user": request.user,
        "student": student
    }
    
    return render(request, 'dashboard/base.html', context)
    # return HttpResponse("Welcome new student")

@login_required
@category_check_factory_dectorator('student')
def complete_profile(request):
    institutions = Institution.objects.all()
    context = {
        "user": request.user,
        "institutions": institutions
    }

    if request.method == "POST":
        user = User.objects.filter(email=request.user)
        Student(
            user = request.user,
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            institution_id = request.POST["institution"],
            faculty_id = request.POST["faculty"],
            department_id = request.POST["department"],
            tel = request.POST["tel"],
            referral_code = generate_referral_code("S")
        ).save()
    return render(request, 'student/complete-profile.html', context)

@profile_completion_redirect
@login_required
def profile(request):
    student = Student.objects.get(user=request.user)
    context = {
        "user": request.user,
        "student": student
    }
    return render(request, 'student/profile.html', context)


@category_check_factory_dectorator('student')
@profile_completion_redirect
@login_required
def edit_profile(request):
    if request.method == "POST":
        filename = None
        if request.FILES["profile-pic"]:
            fs = FileSystemStorage()
            file = request.FILES["profile-pic"]
            filename = fs.save(file.name, file)
            
        Student.objects.filter(user=request.user).update(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            institution_id = request.POST["institution"],
            faculty_id = request.POST["faculty"],
            department_id = request.POST["department"],
            tel = request.POST["tel"],
            referral_code = generate_referral_code("S"),
            profile_pic = filename
        )
        return HttpResponseRedirect(reverse('student:profile'))

    student = Student.objects.get(user=request.user)
    institutions = Institution.objects.all()
    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    print(student.profile_pic.url, "*********")
    context = {
        "user" : request.user,
        "student" : student,
        "institutions" : institutions,
        "faculties" : faculties,
        "departments" : departments
    }
    
    return render(request, 'student/edit-profile.html', context)

@category_check_factory_dectorator('student')
@profile_completion_redirect
@login_required
def my_courses(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'student/my-courses.html')
    