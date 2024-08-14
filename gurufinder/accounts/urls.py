from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SignUpView, StudentSignUpView, TutorSignUpView, ProfileView, ProfileUpdateView, TutorBookedSession, ActiveSession
from . import views as acccount_views

app_name = 'accounts'
urlpatterns = [
    path('signup/', include([
        path('', SignUpView.as_view(), name='signup'),
        path('student/', StudentSignUpView.as_view(), name='student_signup'),
        path('tutor/', TutorSignUpView.as_view(), name='tutor_signup'),
    ])),
    path('student-wallet/', acccount_views.student_wallet, name='student_wallet'),
    path('tutor-wallet/', acccount_views.tutor_wallet, name='tutor_wallet'),
    # path('student-wallet/add-amount/', acccount_views.student_add_amount, name='student_add_amount'),
    path('booked-sessions/', ActiveSession.as_view(), name='booked_sessions'),
    path('booked-sessions/end-session/<int:id>/', acccount_views.end_session, name='end_session'),
    path('end-session-rating-student/<int:id>/', acccount_views.end_session_rating_student, name='end_session_rating_student'),
    path('end-session-rating-tutor/<int:id>/', acccount_views.end_session_rating_tutor,name='end_session_rating_tutor'),
    path('booked-requests/', TutorBookedSession.as_view(), name='tutor_bookings'),
    path('booked-requests/deny/<int:id>/', acccount_views.deny_request, name='deny_request'),
    path('booked-requests/accept/<int:id>/', acccount_views.accept_request, name='accept_request'),
    path('availability/', acccount_views.availability, name='availability'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<username>/', ProfileUpdateView.as_view(), name='profile_update'),
]