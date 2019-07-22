# django related imports
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver

# app related imports
from mainapp.models import Institution, Faculty, Department
from tutor.models import TutorialSession

# system related imports 
from datetime import datetime
import os

def user_directory_path(instance, filename):
    date = datetime.now()
    print("Hello world. Just testing here", "******************")
    return "student/user_{0}/{1}/{2}/{3}/{4}".format(instance.user.id, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), filename)

# Create your models here.
class TemporaryStudentRegistration(models.Model):
    email = models.EmailField()
    secret_token = models.CharField(max_length=124)

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    courses = ArrayField(models.CharField(max_length=20), null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    referral_code = models.CharField(max_length=12)
    points = models.BigIntegerField(default=0)
    tel = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True)

    def __str__(self):
        return self.first_name + self.last_name

class BookedTutorialSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    tutorial_session = models.ForeignKey(TutorialSession, on_delete=models.PROTECT)

@receiver(models.signals.post_delete, sender=Student)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # remove the file from the file system with os.remove
    # if the file is in the file system 
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)

@receiver(models.signals.pre_save, sender=Student)
def auto_delete_on_pre_save(sender, instance, **kwargs):
    # check to see the instance already exists in the db
    # compare the old file to the incoming file if they are thesame
    # delete if they are not
    print("I am here")
    if not instance.pk:
        return False
    try:
        old_file = Student.objects.get(pk=instance.pk).profile_pic
        print("I got the old file")
    except Student.DoesNotExist as e:
        print(e)
        return False
    
    new_file = instance.profile_pic
    print("I got the new file")
    if not new_file == old_file:
        print("Old file and new file are not equal")
        if os.path.isfile(old_file.path):
            print("Old file is a file")
            os.remove(old_file.path)
            print("Removed from file system")
    else:
        print(
            "Old and file and new file are equal"
        )
