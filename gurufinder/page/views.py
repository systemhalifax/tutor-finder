from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from page.models import Page, PostFileContent
from classroom.models import Subject
from module.models import Module
from completion.models import Completion

from page.forms import NewPageForm


@login_required
def new_page_module(request, **kwargs):
	user = request.user
	subject = Subject.objects.get(id=kwargs.get('subject_id'))
	module = Module.objects.get(id=kwargs.get('module_id'))
	id = kwargs.get('subject_id')
	files_objs = []

	if user != subject.classroom.bookings.tutor_id.user:
		return HttpResponseForbidden()

	else:
		if request.method == 'POST':
			form = NewPageForm(request.POST, request.FILES)
			if form.is_valid():
				title = form.cleaned_data.get('title')
				content = form.cleaned_data.get('content')
				files = request.FILES.getlist('files')

				for file in files:
					file_instance = PostFileContent(file=file, user=user)
					file_instance.save()
					files_objs.append(file_instance)

				p = Page.objects.create(title=title, content=content, user=user)
				p.files.set(files_objs)
				p.save()
				module.pages.add(p)
				return redirect('classroom:modules', slug=subject.slug, subject_id=id)
		else:
			form = NewPageForm()
	context = {
		'form': form,
	}

	return render(request, 'page/newpage.html', context)


def page_detail(request, **kwargs):
	subject_id = kwargs.get('subject_id')
	module_id = kwargs.get('module_id')
	page_id = kwargs.get('page_id')
	page = Page.objects.get(id=page_id)
	subject = Subject.objects.get(id=subject_id)
	completed = Completion.objects.filter(subject_id=subject_id, user=request.user, page_id=page_id).exists()

	context = {
		'page': page,
		'completed': completed,
		'subject_id': subject_id,
		'module_id': module_id,
		'subject':subject,
	}
	return render(request, 'page/page.html', context)

def mark_page_as_done(request, **kwargs):
	user = request.user
	subject_id = kwargs.get('subject_id')
	module_id = kwargs.get('module_id')
	page_id = kwargs.get('page_id')
	page = Page.objects.get(id=page_id)
	subject = Subject.objects.get(id=subject_id)
	Completion.objects.create(user=user, subject=subject, page=page)

	return redirect('classroom:modules', slug=subject.slug, subject_id=subject_id)
