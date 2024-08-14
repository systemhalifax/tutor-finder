from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, TutorProfile, Application


#import signals on apps.py for signals to work
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        else:
            TutorProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_student:
        instance.student_profile.save()
    else:
        instance.tutor_profile.save()


@receiver(post_save, sender=User)
def create_application(sender, instance, created, **kwargs):
    if created:
        if instance.is_tutor:
            Application.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_tutor:
        instance.tutor_form.save()


# @receiver(post_save, sender=User)
# def save_application(sender, instance, **kwargs):
#     if instance.is_tutor:
#         instance.