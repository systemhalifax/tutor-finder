from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from assignment.forms import NewAssignmentForm, NewSubmissionForm
from assignment.models import AssignmentFileContent, Assignment, Submission

from module.models import Module
from classroom.models import Subject, Grade
from completion.models import Completion


# Create your views here.
def new_assignment(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    module_id = kwargs.get('module_id')
    subject = Subject.objects.get(id=subject_id)
    module = Module.objects.get(id=module_id)
    files_objs = []

    if user != subject.classroom.bookings.tutor_id.user:
        return HttpResponseForbidden()
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                points = form.cleaned_data.get('points')
                due = form.cleaned_data.get('due')
                files = request.FILES.getlist('files')

                for file in files:
                    file_instance = AssignmentFileContent(file=file, user=user)
                    file_instance.save()
                    files_objs.append(file_instance)

                a = Assignment.objects.create(title=title, content=content, points=points, due=due, user=user)
                a.files.set(files_objs)
                a.save()
                module.assignments.add(a)
                return redirect('classroom:modules', slug=subject.slug, subject_id=subject.id)
        else:
            form = NewAssignmentForm()

    context = {
        'form': form,
    }
    return render(request, 'assignment/newassignment.html', context)


def assignment_detail(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    module_id = kwargs.get('module_id')
    assignment_id = kwargs.get('assignment_id')
    subject = Subject.objects.get(id=subject_id)
    assignment = Assignment.objects.get(id=assignment_id)
    my_submissions = Submission.objects.filter(assignment=assignment, user=user)

    context = {
        'assignment': assignment,
        'subject': subject,
        'my_submissions': my_submissions,
        'module_id': module_id,
    }
    return render(request, 'assignment/assignment.html', context)


def new_submission(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    module_id = kwargs.get('module_id')
    assignment_id = kwargs.get('assignment_id')
    subject = Subject.objects.get(id=subject_id)
    assignment = Assignment.objects.get(id=assignment_id)

    if request.method == 'POST':
        form = NewSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('file')
            comment = form.cleaned_data.get('comment')
            s = Submission.objects.create(file=file, comment=comment, user=user, assignment=assignment)
            Grade.objects.create(subject=subject, submission=s)
            Completion.objects.create(user=user, subject=subject, assignment=assignment)
            return redirect('classroom:modules', slug=subject.slug, subject_id=subject.id)
    else:
        form = NewSubmissionForm()
    context = {
        'form': form,
        'assignment': assignment,
    }
    return render(request, 'assignment/submitassignment.html', context)
