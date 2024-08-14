from accounts.models import User, TutorProfile, StudentProfile, Bookings
from classroom.models import Lesson
from django import template
register = template.Library()


@register.filter(name='tutor_students')
def get_tutor(id):
    tutor = TutorProfile.objects.get(id=id)
    return tutor.students


@register.filter(name='my_students')
def get_student(id):
    student = StudentProfile.objects.get(id=id)
    return student.user.username


@register.filter(name='book_counter')
def book_counter(id):
    tutor = User.objects.get(id=id)
    active_session = Bookings.objects.filter(tutor_id=tutor.tutor_profile, on_session=False)

    return active_session.count()


# @register.filter(name='filter_bookings_tutor')
# def filter_bookings_tutor(id):
#     tutor = User.objects.get(id=id)
#     active_session = Bookings.objects.filter(tutor_id=tutor.tutor_profile, on_session=True)
#
#     return active_session
#
#
# @register.filter(name='filter_bookings_tutor')
# def filter_bookings_tutor(id):
#     tutor = User.objects.get(id=id)
#     active_session = Bookings.objects.filter(tutor_id=tutor.tutor_profile, on_session=True)
#
#     return active_session


# @register.filter(name='check_completed')
# def check_if_completed(id):
#     lesson = Lesson.objects.get(id=id)
#     return lesson.completed
