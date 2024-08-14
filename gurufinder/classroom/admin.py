from django.contrib import admin
from .models import Classroom, Subject, Lesson, Comment, Reply, WorkingDays, TimeSlots, SlotSubject

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(WorkingDays)
admin.site.register(TimeSlots)
admin.site.register(SlotSubject)
