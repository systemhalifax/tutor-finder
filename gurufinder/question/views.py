from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator

from question.models import Question, Answer, Votes
from question.forms import QuestionForm, AnswerForm

from classroom.models import Subject


def new_student_question(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    #subjects = Subject.objects.get(id=subject_id)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            q = Question.objects.create(user=user, title=title, body=body)
            #subject.questions.add(q)
            for subject in subjects:
                subject.questions.add(q)
            return redirect('classroom:questions', slug=subject.slug, subject_id=subject.id)
    else:
        form = QuestionForm()
    context = {
        'form': form,
    }
    return render(request, 'question/newquestion.html', context)


def questions(request, **kwargs):
    subject_id = kwargs.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    questions = subject.questions.all()

    # Pagination
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    questions_data = paginator.get_page(page_number)

    context = {
        'subject': subject,
        'questions': questions_data,
    }
    return render(request, 'question/questions.html', context)


def question_detail(request, **kwargs):
    user = request.user
    # moderator = False
    question_id = kwargs.get('question_id')
    subject_id = kwargs.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    question = Question.objects.get(id=question_id)

    correct_answer = Answer.objects.filter(question=question, is_accepted_answer=True)
    rest_answers = Answer.objects.filter(question=question)

    answers = correct_answer | rest_answers

    # if user == subject.classroom.bookings.tutor_id.user or user == question.user:
    #     moderator = True

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            Answer.objects.create(user=user, question=question, body=body)
            return redirect('classroom:question-detail', slug=subject.slug, subject_id=subject_id, question_id=question_id)
    else:
        form = AnswerForm()
    context = {
        'question': question,
        'answers': answers,
        'subject': subject,
        'form': form,
        # 'moderator': moderator,
    }
    return render(request, 'question/question.html', context)


def mark_as_answer(request, **kwargs):
    user = request.user
    answer_id = kwargs.get('answer_id')
    question_id = kwargs.get('question_id')
    subject_id = kwargs.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    question = Question.objects.get(id=question_id)

    if user == subject.classroom.bookings.tutor_id.user or user == question.user:
        answer = Answer.objects.get(id=answer_id)
        answer.is_accepted_answer = True
        answer.save()
        question.has_accepted_answer = True
        question.save()
        return redirect('classroom:question-detail', slug=subject.slug, subject_id=subject_id, question_id=question_id)
    else:
        return HttpResponseForbidden()


def vote_answer(request, **kwargs):
    user = request.user
    subject_id = kwargs.get('subject_id')
    question_id = kwargs.get('question_id')
    answer_id = request.POST['answer_id']
    vote_type = request.POST['vote_type']
    try:
        answer = Answer.objects.get(id=answer_id)
        voted = Votes.objects.filter(user=user, answer=answer)
        if voted:
            voted.delete()
        else:
            if vote_type == 'U':
                Votes.objects.create(user=user, answer=answer, vote='U')
            else:
                Votes.objects.create(user=user, answer=answer, vote='D')
        return HttpResponse(answer.calculate_votes())
    except Exception as e:
        raise e