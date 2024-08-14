from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from accounts.models import Bookings
import os

from module.models import Module
from assignment.models import Submission
from question.models import Question


from django.contrib.auth import get_user_model
User = get_user_model()
# from django.conf import settings
# User = settings.AUTH_USER_MODEL


class Classroom(models.Model):
    bookings = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)


class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, related_name='subjects')
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500, blank=True)
    modules = models.ManyToManyField(Module, blank=True)
    questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return f'{self.classroom}-{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)


class Grade(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('graded', 'Graded'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=10, verbose_name='Status')


def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    if instance.lesson_id:
        filename = f'lesson_files/{instance.lesson_id}/{instance.lesson_id}.{ext}'
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename = f'lesson_images/{instance.lesson_id}/{new_name}.{ext}'
    return os.path.join(upload_to, filename)


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    Classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True,)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(default='None', null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files, verbose_name="Video", blank=True, null=True)
    ppt = models.FileField(upload_to=save_lesson_files, verbose_name="Presentations", blank=True)
    Notes = models.FileField(upload_to=save_lesson_files, verbose_name="Notes", blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.Classroom}-{self.name}'

    def save(self, *args, **kwargs):
        if self.slug == 'None':
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    #for redirecting purposes
    def get_absolute_url(self):
        return reverse('classroom:lesson_list', kwargs={'slug': self.subject.slug, 'classroom': self.Classroom.slug})


class WorkingDays(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, related_name='classroom_days')
    day = models.CharField(max_length=100)

    def __str__(self):
        return self.day


class TimeSlots(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, related_name='classroom_time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time)


class SlotSubject(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, blank=True, related_name='classroom_slots')
    day = models.ForeignKey(WorkingDays, on_delete=models.CASCADE, related_name='classroom_slots_days')
    slot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE, related_name='classroom_slots_time')
    slot_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classroom_slots_subject')

    def __str__(self):
        return str(self.classroom) + ' - ' + str(self.day) + ' - ' + str(self.slot) + ' - ' + str(self.slot_subject)


class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson,null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']


class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)