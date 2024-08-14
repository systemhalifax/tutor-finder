from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy
from module.forms import NewModuleForm
from module.models import Module
from classroom.models import Subject

from completion.models import Completion
# Create your views here.

def new_module(request, **kwargs):
	user = request.user
	subject = Subject.objects.get(id=kwargs.get('subject_id'))
	id = kwargs.get('subject_id')

	if user != subject.classroom.bookings.tutor_id.user:
		return HttpResponseForbidden()
	else:
		if request.method == 'POST':
			form = NewModuleForm(request.POST)
			if form.is_valid():
				title = form.cleaned_data.get('title')
				hours = form.cleaned_data.get('hours')
				m = Module.objects.create(title=title, hours=hours, user=user)
				subject.modules.add(m)
				subject.save()
				return redirect('classroom:modules', slug=subject.slug, subject_id=id)

		else:
			form = NewModuleForm()

	context = {
		'form': form,
	}

	return render(request, 'module/newmodule.html', context)



def course_modules(request, **kwargs):
	user = request.user
	subject = Subject.objects.get(id=kwargs.get('subject_id'))

	page_completions = Completion.objects.filter(user=user, subject=subject).values_list('page__pk', flat=True)
	quiz_completions = Completion.objects.filter(user=user, subject=subject).values_list('quiz__pk', flat=True)
	assignment_completions = Completion.objects.filter(user=user, subject=subject).values_list('assignment__pk', flat=True)


	context = {
		'subject': subject,
		'page_completions': page_completions,
		'quiz_completions': quiz_completions,
		'assignment_completions': assignment_completions,
	}

	return render(request, 'module/modules.html', context)