from django.contrib import admin
from .models import User, TutorProfile, StudentProfile, Transactions, Bookings

admin.site.register(User)
admin.site.register(TutorProfile)
admin.site.register(StudentProfile)
admin.site.register(Bookings)
admin.site.register(Transactions)

