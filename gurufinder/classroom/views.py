from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView
from .models import Classroom, Subject, Lesson, TimeSlots, Grade
from django.urls import reverse_lazy
from .forms import CommentForm, ReplyForm, LessonForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from completion.models import Completion


class ClassroomListView(ListView):
    context_object_name = 'classrooms'
    model = Classroom
    template_name = 'classroom/classroom_list_view.html'


# class SubjectListView(DetailView):
#     context_object_name = 'classrooms'
#     extra_context = {
#         'slots': TimeSlots.objects.all()
#     }
#     model = Classroom
#     template_name = 'classroom/subject_list_view.html'


class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'classroom/lesson_list_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LessonListView, self).get_context_data(*args, **kwargs)
        user = self.object.classroom.bookings.student_id.user
        subject = self.object.id
        context['lesson_completions'] = Completion.objects.filter(user=user, subject=subject).values_list('lesson__pk', flat=True)

        return context


class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'classroom/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        subject = self.object.subject
        lesson = self.object.id
        context['completed'] = Completion.objects.filter(subject=subject.id, user=self.request.user, lesson=lesson).exists()

        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name == 'form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        classroom = self.object.Classroom
        subject = self.object.subject
        return reverse_lazy('classroom:lesson_detail', kwargs={'classroom': classroom.slug, 'subject': subject.slug, 'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

def mark_lesson_as_done(request, **kwargs):
	user = request.user
	subject_id = kwargs.get('subject_id')
	lesson_id = kwargs.get('lesson_id')
	lesson = Lesson.objects.get(id=lesson_id)
	subject = Subject.objects.get(id=subject_id)
	Completion.objects.create(user=user, subject=subject, lesson=lesson)

	return redirect('classroom:lesson_list', slug=subject.slug, subject_id=subject_id)


class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'subject'
    model = Subject
    template_name = 'classroom/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        classroom = self.object.classroom
        return reverse_lazy('classroom:lesson_list', kwargs={'slug': self.object.slug, 'subject_id': self.object.id})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Classroom = self.object.classroom
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonUpdateView(UpdateView):
    fields = ['name', 'position', 'video', 'ppt', 'Notes']
    model = Lesson
    template_name = 'classroom/lesson_update.html'
    context_object_name = 'lessons'


class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'classroom/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        classroom = self.object.Classroom
        subject = self.object.subject
        return reverse_lazy('classroom:lesson_list', kwargs={'classroom': classroom.slug, 'slug': subject.slug})


def lesson_completed(request, **kwargs):
    lesson = Lesson.objects.get(id=kwargs.get('lesson_id'))

    if 'completed' in request.POST:
        lesson.completed = True
        lesson.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif 'not_completed' in request.POST:
        lesson.completed = False
        lesson.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'classroom/lesson_detail_view.html')


# def lesson_not_completed(request, **kwargs):
#     lesson = Lesson.objects.get(id=kwargs.get('id'))
#     print('executed not completed')
#     print(request.POST)
#     print(request.POST)
#     if 'submit' in request.POST:
#         if 'not_completed' == request.POST.get('submit'):
#             lesson.completed = False
#             lesson.save()
#
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#     return render(request, 'classroom/lesson_detail_view.html')

class SubjectListView(DetailView):
    context_object_name = 'classrooms'
    extra_context = {
        'slots': TimeSlots.objects.all()
    }
    model = Classroom
    template_name = 'classroom/subject_list_view.html'


@login_required
def course_detail(request, **kwargs):
	user = request.user
	subject = Subject.objects.get(id=kwargs.get('subject_id'))

	context = {
		'subject': subject,
	}

	return render(request, 'classroom/course.html', context)


def submissions(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    grades = Grade.objects.filter(subject=subject, submission__user=user)
    context = {
		'grades': grades,
		'subject': subject
	}
    return render(request, 'classroom/submissions.html', context)


def student_submissions(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    if user != subject.classroom.bookings.tutor_id.user:
	    return HttpResponseForbidden()
    else:
        grades = Grade.objects.filter(subject=subject)
        context = {
			'subject': subject,
			'grades': grades,
        }
    return render(request,'classroom/studentgrades.html', context)


def grade_submission(request, **kwargs):
    user = request.user
    grade_id = kwargs.get('grade_id')
    subject_id = kwargs.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    grade = Grade.objects.get(id=grade_id)

    if user != subject.classroom.bookings.tutor_id.user:
	    return HttpResponseForbidden()
    else:
	    if request.method == 'POST':
		    points = request.POST.get('points')
		    grade.points = points
		    grade.status = 'graded'
		    grade.graded_by = user
		    grade.save()
		    return redirect('classroom:student-submissions', slug=subject.slug, subject_id=subject.id)
    context = {
		'subject': subject,
		'grade': grade,
	}

    return render(request, 'classroom/gradesubmission.html', context)
