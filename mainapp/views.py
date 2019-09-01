#system related imports
import secrets
from decouple import config
import smtplib
import random
import math

# django related imports
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.urls import reverse
from django.template.loader import render_to_string

# application related imports
from student.models import TemporaryStudentRegistration
from tutor.models import TemporaryTutorRegistration
from .models import User, Faculty, Department
from student.models import Student
from tutor.models import Tutor

# Create your views here.
def category_check_factory_dectorator(category):
    def category_check_decorator(func):
        # use this function as decorator to
        # check to make sure the link accessed by
        # the user is the right one to access (SECURITY)
        # e.g lets say the user a student on the home page (the url is /student/home/)
        # if the user changes to /tutor/home/, use this decorator to redirect back to
        # /student/home/
        def inner(*args, **kwargs):
            groups = list(args[0].user.groups.values_list('name',flat=True))
            if category == "student":
                if "students" in groups:
                    return func(*args, **kwargs)
                else:
                    # TODO: display the 404 unauthorised page
                    return HttpResponse("You are unauthorised to access tutor page as student")
            if category == "tutor":
                if "tutors" in groups:
                    print(func)
                    return func(*args, **kwargs)
                else:
                    # TODO: display the 404 unauthorised page
                    return HttpResponse("You are unauthorised to access student page as tutor")
        return inner
    return category_check_decorator

def tutor_application_redirect(func):
    # use this function as decorator to
    # redirect the tutor to the application
    # status page
    def inner(*args, **kwargs):
        tutor = Tutor.objects.get(user=args[0].user)
        context = {
            "application_status" : tutor.application_status,
        }
        if tutor.application_status == "approved":
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('tutor:application-status'))
    return inner

def homepage(request):
    template_name = "mainapp/index.html"
    if request.user.is_authenticated:
        groups = list(request.user.groups.values_list('name',flat=True))
        # checking if the user belongs to the student or tutor group
        # redirection will take place based on which group the user belongs
        if "students" in groups:
            return HttpResponseRedirect(reverse('student:home'))
        if "tutors" in groups:
            return HttpResponseRedirect(reverse('tutor:home'))

    return render(request, template_name)

def pre_registration(request):
    email = request.POST["email"]
    category = request.POST["category"]
    
    # test to see if the user has already registered by checking the User object
    user = User.objects.filter(email=email)
    if user.exists():
        return HttpResponse("This email is already registered", status=404)

    # send a secret token via email to be used by student to complete registration process
    if category == "student":
        secret_token = generate_token("student")
        activation_link = request.build_absolute_uri('/')+"complete-registration/?email="+email+"&category=student"+"&key="+secret_token
        subject = "MyTutz Registration"
        msg = "Click " + activation_link + " to complete your student registration to MyTutz"

        try:
            print('testing ', email)
            send_mail(subject, msg, "Sone Gillis at MyTutz", [email,], False)
            print('testing2')
            TemporaryStudentRegistration(
                email = email,
                secret_token = secret_token
            ).save()
            return HttpResponse("")
        except smtplib.SMTPException as e:
            return HttpResponse("Failed to send a secret token link. Perform the action again", status=404)
    
    # send a secret token via email to be used by tutors to complete registration process
    if category == "tutor":
        secret_token = generate_token("tutor")
        activation_link = request.build_absolute_uri('/')+"complete-registration/?email="+email+"&category=tutor"+"&key="+secret_token
        subject = "MyTutz Registration"
        msg = "Click " + activation_link + " to complete your tutor registration to MyTutz"
        try:
            send_mail(subject, msg, "Sone Gillis at MyTutz", [email,], False)
            TemporaryTutorRegistration(
                email = email,
                secret_token = secret_token
            ).save()
            return HttpResponse("")
        except smtplib.SMTPException as e:
            return HttpResponse("Failed to send a secret token link. Perform the action again", status=404)            
        
def complete_registration(request):
    secret_token = request.GET.get('key', '')
    category = request.GET.get('category', '')
    if request.method == "GET":
        email = request.GET.get('email', '')
        if category == "student":
            # check for the validity of the email and key combination from the database
            temp_student = TemporaryStudentRegistration.objects.filter(Q(email=email) & Q(secret_token=secret_token))
            user = User.objects.filter(email=email)
            # if valid then prompt for complete registration and the email is not yet registered
            if temp_student.exists() and not user.exists():
                template_name = "mainapp/complete_registration.html"
                return render(request, template_name, {"email": email, "category": category.upper()})
            # else display denial alert to the user
            else:
                return HttpResponse("Sorry but you cannot login")
        if category == "tutor": 
            # check for the validity of the email and key combination from the database
            temp_tutor = TemporaryTutorRegistration.objects.filter(Q(email=email) & Q(secret_token=secret_token))
            user = User.objects.filter(email=email)
            # if valid then prompt for complete registration and the email is not yet registered
            if temp_tutor.exists() and not user.exists():
                template_name = "mainapp/complete_registration.html"
                return render(request, template_name, {"email": email, "category": category.upper()})
            # else display denial alert to the user
            else:
                return HttpResponse("Sorry but you cannot login")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password1"]

        user = User.objects.create_user(
                email = email,
                password = password
            )
        # add the user to the student or tutor group
        group = Group.objects.get(name=category+"s") 
        group.user_set.add(user)

        user = authenticate(email=email, password=password)
        if category == "student":
            TemporaryStudentRegistration.objects.filter(email=email).delete()
        if category == "tutor":
            TemporaryTutorRegistration.objects.filter(email=email).delete()
        login(request, user)
        return HttpResponseRedirect(reverse(category+":home"))
        
def user_login(request):
    email = request.POST["signin_email"]
    password = request.POST["password"]
    user = authenticate(email=email, password=password)

    if user is not None:
        login(request, user)
        groups = list(user.groups.values_list('name',flat=True))

        # checking if the user belongs to the student or tutor group
        # redirection will take place based on which group the user belongs
        if "students" in groups:
            return HttpResponse(reverse('student:home'))
        if "tutors" in groups:
            return HttpResponse(reverse('tutor:home'))
    else:
        print(email, password)
        return HttpResponse("", status=404)

def get_faculty_options(request):
    print(request.GET["institution"])
    faculties = Faculty.objects.filter(institution__id=request.GET["institution"])
    print(faculties);
    return HttpResponse(render_to_string("dashboard/faculty-options.html", {"faculties": faculties}))

def get_department_options(request):
    departments = Department.objects.filter(faculty__id=request.GET["faculty"])
    return HttpResponse(render_to_string("dashboard/department-options.html", {"departments": departments}))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def sendEmail(destination_email, email_text):
    """
    arguments
    ---------
        destination_email: the email to which the mail is going to
        email_text: the actual mail

    return
    ------
        success: if the mail was successfully sent
        error: if the mail was not sent
    """

    gmail_user = config('senders_email')
    gmail_password = config('senders_password')

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, destination_email, email_text)
        server.close()
        return "success"
    except Exception as e:
        print(e)
        return "error"

def generate_token(category):
    """
        return
        ------
        secret_token: the 124 character unique key generated
    """
    while(True):
        secret_token = secrets.token_urlsafe(60);
        qs = TemporaryStudentRegistration.objects.filter(secret_token=secret_token)
        qs1 = TemporaryTutorRegistration.objects.filter(secret_token=secret_token)
        if not qs.exists() and not qs1.exists():
            break
    return secret_token
        
def verify_email(request):
    """
        return
        ------
        allow_email:javascript would use this at the client to determine if client has put a validated email or not
    """
    allow_email = "false"
    user = User.objects.filter(email=request.POST["email"])
    if not user.exists():
        allow_email = "true"
    return HttpResponse(allow_email)

def generate_referral_code(category):
    """
        arguments
        ---------
        category: Determines if the referral code is for student (S) or tutor (T)

        return
        ------
        referral_code: a randomly generated referral code
    """
    if category is "S":
        while(True):
            referral_code = "S-"+str(math.floor(random.random()*1000000))
            if not Student.objects.filter(referral_code=referral_code).exists():
                break
        
    if category is "T":
        while(True):
            referral_code = "T-"+str(math.floor(random.random()*1000000))
            if not Tutor.objects.filter(referral_code=referral_code).exists():
                break

    return referral_code