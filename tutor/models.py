# django related imports
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver

# app related imports
from mainapp.models import Institution, Faculty, Department

# system related imports 
from datetime import datetime
import os

application_status = [
    ["pending", "pending"],
    ["approved", "approved"],
    ["refused", "refused"]
]

def user_directory_path(instance, filename):
    date = datetime.now()
    print("Hello world. Just testing here", "******************")
    return "tutor/user_{0}/{1}/{2}/{3}/{4}".format(instance.user.id, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), filename)

# Create your models here
class TemporaryTutorRegistration(models.Model):
    email = models.EmailField()
    secret_token = models.CharField(max_length=124)

class Tutor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    courses = ArrayField(models.CharField(max_length=20), null=True)
    referral_code = models.CharField(max_length=12)
    points = models.BigIntegerField(default=0)
    tel = models.CharField(max_length=30)
    application_status = models.CharField(choices=application_status, max_length=50, default="pending")
    education_level = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True)
    transcript = models.FileField(upload_to=user_directory_path, null=True)
    cv = models.FileField(upload_to=user_directory_path, null=True)
    application_viewed = models.BooleanField(default=False)     # this will be set to true when the application_status has been updated

    def __str__(self):
        return self.first_name + self.last_name

@receiver(models.signals.post_delete, sender=Tutor)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # remove the file from the file system with os.remove
    # if the file is in the file system 
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)
    if instance.transcript:
        if os.path.isfile(instance.transcript.path):
            print(instance.transcript.path)
            os.remove(instance.transcript.path)
    if instance.cv:
        if os.path.isfile(instance.cv.path):
            os.remove(instance.cv.path)

@receiver(models.signals.pre_save, sender=Tutor)
def auto_delete_on_pre_save(sender, instance, **kwargs):
    # check to see the instance already exists in the db
    # compare the old file to the incoming file if they are thesame
    # delete if they are not
    print("I am here")
    if not instance.pk:
        return False
    try:
        old_file1 = Tutor.objects.get(pk=instance.pk).profile_pic
        old_file2 = Tutor.objects.get(pk=instance.pk).transcript
        old_file3 = Tutor.objects.get(pk=instance.pk).cv
        print("I got the old file")
    except Tutor.DoesNotExist as e:
        print(e)
        return False
    
    new_file1 = instance.profile_pic
    new_file2 = instance.transcript
    new_file3 = instance.cv
    print("I got the new file")
    if not new_file1 != old_file1:
        print("Old file and new file are not equal")
        if os.path.isfile(old_file1.path):
            print("Old file is a file")
            os.remove(old_file1.path)
            print("Removed from file system")
    else:
        print("Old and file and new file are equal")
    if not new_file2 != old_file2:
        print("Old file and new file are not equal")
        if os.path.isfile(old_file2.path):
            print("Old file is a file")
            os.remove(old_file2.path)
            print("Removed from file system")
    else:
        print("Old and file and new file are equal")
    if not new_file3 != old_file3:
        print("Old file and new file are not equal")
        if os.path.isfile(old_file3.path):
            print("Old file is a file")
            os.remove(old_file3.path)
            print("Removed from file system")
    else:
        print("Old and file and new file are equal")