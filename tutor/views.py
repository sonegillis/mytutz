# django related imports
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

# app related imports
from .models import Tutor
from mainapp.models import Institution, Faculty, Department, User
from mainapp.views import generate_referral_code, category_check_factory_dectorator, tutor_application_redirect

#system related imports 
import math
import random

# Create your views here.
def profile_completion_redirect(func):
    # use this function as decorator to
    # redirect to complete profile or not based on if the 
    # his student entry has been recorded
    def inner(*args, **kwargs):
        if Tutor.objects.filter(user=args[0].user).exists():
            httpResponse = func(*args, **kwargs)
            return httpResponse
        else: 
            return HttpResponseRedirect(reverse('tutor:complete-profile'))
    return inner

@login_required
@profile_completion_redirect
@category_check_factory_dectorator('tutor')
@tutor_application_redirect
def home(request):
    # if prompt_profile_completion(request.user):
    #     return HttpResponseRedirect(reverse('student:complete-profile'))
    tutor = Tutor.objects.filter(user = request.user)
    context = {
        "user": request.user,
        "tutor": tutor
    }
    
    return render(request, 'dashboard/base.html', context)

@category_check_factory_dectorator('tutor')
@login_required
def complete_profile(request):
    institutions = Institution.objects.all()
    context = {
        "user": request.user,
        "institutions": institutions
    }

    if request.method == "POST":
        user = User.objects.filter(email=request.user)
        courses = [course.strip() for course in request.POST["courses"].split(",") if course.strip() != ""]
        print(request.FILES)
        Tutor(
            user = request.user,
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            institution_id = request.POST["institution"],
            tel = request.POST["tel"],
            referral_code = generate_referral_code("T"),
            courses = courses,
            profile_pic = request.FILES["profile_pic"],
            education_level = request.POST["qualification"],
            transcript = request.FILES["transcript"],
            cv = request.FILES["cv"]
        ).save()
        return HttpResponseRedirect(reverse('tutor:application-status'))
    return render(request, 'tutor/complete-profile.html', context)

@category_check_factory_dectorator('tutor')
@profile_completion_redirect
@tutor_application_redirect
@login_required
def profile(request):
    tutor = Tutor.objects.get(user=request.user)
    context = {
        "user": request.user,
        "tutor": tutor
    }
    return render(request, 'tutor/profile.html', context)

@category_check_factory_dectorator('tutor')
@profile_completion_redirect
@tutor_application_redirect
@login_required
def edit_profile(request):
    if request.method == "POST":
        fs = FileSystemStorage()
        file = request.FILES["profile-pic"]
        profile_pic = fs.save(file.name, file)
        file = request.FILES["transcript"]
        transcript = fs.save(file.name, file)
        file = request.FILES["cv"]
        cv = fs.save(file.name, file)
            
        Tutor.objects.filter(user=request.user).update(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            institution_id = request.POST["institution"],
            tel = request.POST["tel"],
            referral_code = generate_referral_code("S"),
            profile_pic = profile_pic,
            courses = courses,
            qualification = request.POST["qualification"],
            transcript = transcript,
            cv = request.FILES["cv"]
        )
        return HttpResponseRedirect(reverse('tutor:profile'))

    tutor = Tutor.objects.get(user=request.user)
    institutions = Institution.objects.all()
    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    print(tutor.profile_pic.url, "*********")
    context = {
        "user" : request.user,
        "tutor" : tutor,
        "institutions" : institutions,
        "faculties" : faculties,
        "departments" : departments
    }
    
    return render(request, 'tutor/edit-profile.html', context)

def application_status(request):
    tutor = Tutor.objects.get(user=request.user)
    context = {
        "application_status" : tutor.application_status,
        "tutor" : tutor
    }
    # print(tutor.profile_pic.url)
    if tutor.application_status == "pending": context["text_color"] = "text-primary"
    if tutor.application_status == "denied":  context["text-color"] = "text-danger" 
    if tutor.application_status == "success": context["text-color"] = "text-success"

    return render(request, "tutor/application-status-msg.html", context)

@category_check_factory_dectorator('tutor')
@profile_completion_redirect
@tutor_application_redirect
@login_required
def my_courses(request):
    tutor = Tutor.objects.get(user=request.user)
    return render(request, 'tutor/my-courses.html')