from django.urls import path
from . import views

from module.views import course_modules, new_module
from page.views import new_page_module, page_detail, mark_page_as_done
from quiz.views import new_quiz, new_question, quiz_detail, take_quiz, submit_attempt, attempt_detail
from assignment.views import new_assignment, assignment_detail, new_submission
from question.views import new_student_question, questions, question_detail, mark_as_answer, vote_answer




app_name = 'classroom'
urlpatterns = [
    path('', views.ClassroomListView.as_view(), name='classroom_list'),
    path('<slug:slug>/', views.SubjectListView.as_view(), name='subject_list'),
    path('<slug:slug>/<int:subject_id>/', views.course_detail, name='course'),
    path('<slug:slug>/<int:subject_id>/modules/', course_modules, name='modules'),
    path('<slug:slug>/<int:subject_id>/modules/new-module/', new_module, name='new-module'),
    #pages
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/pages/new-page/', new_page_module, name='new-page'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/pages/<int:page_id>/', page_detail, name='page-detail'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/pages/<int:page_id>/done/', mark_page_as_done, name='mark-page-as-done'),

    #Quizzes
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/quiz/new-quiz', new_quiz, name='new-quiz'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/quiz/<int:quiz_id>/new-question', new_question, name='new-question'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/quiz/<int:quiz_id>/', quiz_detail, name='quiz-detail'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/quiz/<int:quiz_id>/take', take_quiz, name='take-quiz'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/quiz/<int:quiz_id>/take/submit', submit_attempt, name='submit-quiz'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/quiz/<int:quiz_id>/<int:attempt_id>/results', attempt_detail, name='attempt-detail'),

    #Assignment
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/assignment/new-assignment', new_assignment, name='new-assignment'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/assignment/<int:assignment_id>', assignment_detail, name='assignment-detail'),
    path('<slug:slug>/<int:subject_id>/modules/<int:module_id>/assignment/<int:assignment_id>/start', new_submission, name='start-assignment'),

    #Submissions
	path('<slug:slug>/<int:subject_id>/submissions', views.submissions, name='submissions'),
	path('<slug:slug>/<int:subject_id>/student-submissions', views.student_submissions, name='student-submissions'),
	path('<slug:slug>/<int:subject_id>/submissions/<int:grade_id>/grade', views.grade_submission, name='grade-submission'),

    #Questions
    path('<slug:slug>/<int:subject_id>/questions', questions, name='questions'),
    path('<slug:slug>/<int:subject_id>/questions/new-question', new_student_question, name='new-student-question'),
    path('<slug:slug>/<int:subject_id>/questions/<int:question_id>', question_detail, name='question-detail'),
    path('<slug:slug>/<int:subject_id>/questions/<int:question_id>/vote', vote_answer, name='vote-answer'),
    path('<slug:slug>/<int:subject_id>/questions/<int:question_id>/<int:answer_id>/mark-as-answer', mark_as_answer, name='mark-as-answer'),

    #extra content
    path('<slug:slug>/<int:subject_id>/extra-content', views.LessonListView.as_view(), name='lesson_list'),
    path('<slug:slug>/<int:subject_id>/extra-content/create', views.LessonCreateView.as_view(), name='lesson_create'),
    path('<str:classroom>/<str:subject>/extra-content/<slug:slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    # path('<str:classroom>/<str:subject>/extra-content/<slug:slug>/<int:lesson_id>/', views.lesson_completed, name='lesson_complete'),
    # path('<str:classroom>/<str:subject>/<slug:slug>/<int:id>/', views.lesson_not_completed, name='lesson_not_completed'),
    path('<str:classroom>/<str:subject>/extra-content/<slug:slug>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('<str:classroom>/<str:subject>/extra-content/<slug:slug>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
    path('<str:classroom>/<int:subject_id>/extra-content/<int:lesson_id>/mark-as-done/', views.mark_lesson_as_done,name='mark-lesson-as-done'),

]