from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from multiselectfield import MultiSelectField
from star_ratings.models import Rating
import os


def path_and_rename(instance, filename):
    upload_to = 'Images/Profile_Pictures/'
    ext = filename.split('.')[-1]
    if instance.is_student:
        filename = f'Students/{instance.pk}-{instance.first_name} {instance.last_name}.{ext}'
    else:
        filename = f'Tutors/{instance.pk}-{instance.first_name} {instance.last_name}.{ext}'
    return os.path.join(upload_to, filename)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    current_address = models.CharField(max_length=100)
    image = models.ImageField(default='default_pic.jpg', upload_to=path_and_rename, verbose_name='Profile Pictures', blank=True)

    def __str__(self):
        return f'{self.username}'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    has_bookings = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    student_ratings = GenericRelation(Rating, related_query_name='student_ratings')


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profile"


class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile')
    students = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    profile_headline = models.CharField(max_length=200, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    is_validated = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    has_bookings = models.BooleanField(default=False)
    tutor_ratings = GenericRelation(Rating, related_query_name='tutor_ratings')
    # book_counter = models.IntegerField(default=0, null=True, blank=True)
    DAYS = (('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),)

    LANG = (('JavaScript', 'JavaScript'),
            ('Python', 'Python'),
            ('Swift', 'Swift'),
            ('Java', 'Java'),
            ('Sql', 'Sql'),
            ('PHP', 'PHP'),
            ('C#', 'C#'),)

    programming_languages = MultiSelectField(choices=LANG, null=True)
    availability = MultiSelectField(choices=DAYS, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profile"

    def clean(self):
        if self.hourly_rate % 10 != 0:
            raise ValidationError('Hourly rate can only be multiples of 10.')


def save_application_forms(instance, filename):
    upload_to = 'Application_Forms/'
    ext = filename.split('.')[-1]
    if instance:
        filename = f'Portfolio/{instance.user.first_name}.{ext}'
    return os.path.join(upload_to, filename )


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_form')
    valid_id = models.ImageField(upload_to=save_application_forms, blank=True)
    selfie = models.ImageField(upload_to=save_application_forms, blank=True)
    portfolio = models.FileField(upload_to=save_application_forms, blank=True)

    def __str__(self):
        if self.user.tutor_profile.is_validated:
            return f"{self.user.first_name}'s application form (Approved)"
        else:
            return f"{self.user.first_name}'s application form"


class Bookings(models.Model):
    SUB_CHOICES = (('JavaScript', 'JavaScript'),
                   ('Python', 'Python'),
                   ('Swift', 'Swift'),
                   ('Java', 'Java'),
                   ('Sql', 'Sql'),
                   ('PHP', 'PHP'),
                   ('C#', 'C#'),)
    SESSION = (('1', '1 session'),
                   ('2', '2 session'),
                   ('3', '3 session'),
                   ('4', '4 session'),
                   ('5', '5 session'),
               ('0', 'Not sure')
               )
    on_session = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    frequency = models.CharField(max_length=10, choices=SESSION, default='0')
    student_id = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    tutor_id = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=10, choices=SUB_CHOICES, default='JavaScript')
    student_msg = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f'session {self.pk} with {self.tutor_id.user.first_name} and {self.student_id.user.first_name}'


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField()
    added_amount = models.DecimalField(max_digits=8, decimal_places=2)
    subtracted_amount = models.DecimalField(max_digits=8, decimal_places=2)
    details = models.CharField(max_length=256)

    def __str__(self):
        return str(self.user)
