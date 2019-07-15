# django related imports
from django.db import models
from django.dispatch import receiver

# app related imports
import .models import Student

# system related imports
import os

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