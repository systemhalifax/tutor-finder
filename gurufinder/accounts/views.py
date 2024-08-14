from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect,  get_object_or_404
from datetime import datetime, timedelta
from .forms import StudentSignUpForm, TutorSignUpForm, ApplicationForm, TutorProfileForm, BookingsForm, DenyRequestForm, UserUpdateForm #TutorUpdateProfileForm
from django.contrib import messages, admin
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.files.images import ImageFile
from django.core.files import File
from django.conf import settings
from django.views.generic import TemplateView, FormView, ListView, UpdateView, DetailView, CreateView
from .models import User, Application, TutorProfile, StudentProfile, Bookings, Transactions
from django.urls import reverse_lazy, reverse, path
from django_email_verification import send_email
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
import threading
from classroom.models import Classroom, Subject, Lesson
from question.models import Question


def index(request):
    return render(request, 'accounts/index.html')


def about(request):
    return render(request, 'accounts/about.html')


def how_it_works(request):
    return render(request, 'accounts/how_it_works.html')


# def student_wallet(request):
#     return render(request, 'accounts/student_wallet.html')


@login_required
def tutor_wallet(request):

    current_user=request.user
    tutor=get_object_or_404(TutorProfile, user=current_user)
    #transaction for 30 days only
    transaction_list=Transactions.objects.filter(user=current_user).exclude(transaction_time__lt=(datetime.now().date() - timedelta(days=30)))
    print(transaction_list)


    if request.method == 'POST':
        amount_str=request.POST.get("amount")

        if int(amount_str) > tutor.wallet:

            messages.success(request, "You don't have enough balance to transfer!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:

            try:
                amount = (float)(amount_str)
            except:
                amount = 0
                messages.success(request, 'Please enter a valid amount')
                return render(request, 'accounts/tutor_wallet.html', {'tutor': tutor, 'transactions': transaction_list})

            tutor.wallet=(float)(tutor.wallet) - amount
            try:
                tutor.save()

                Transactions.objects.create(user=current_user, transaction_time=datetime.now(), added_amount=0, subtracted_amount=amount, details='Transferred money from wallet')

                messages.success(request,f'Successfully transferred PHP {amount_str} from your wallet!')
                return render(request, 'accounts/tutor_wallet.html', {'tutor': tutor, 'transactions': transaction_list})

            except:
                raise Http404("Oops! Could not add money. Please try again.")

    return render(request, 'accounts/tutor_wallet.html', {'tutor': tutor, 'transactions': transaction_list})



@login_required
def student_wallet(request):

    current_user=request.user
    student=get_object_or_404(StudentProfile, user = current_user)
    transaction_list=Transactions.objects.filter(user = current_user).exclude(transaction_time__lt=(datetime.now().date() - timedelta(days=30)))

    if request.method == 'POST':
        amount_str=request.POST.get("amount")

        try:
            amount=(float)(amount_str)

        except:
            messages.success(request,f"Please enter a valid amount")
            return render(request, 'accounts/student_wallet.html', {'student': student, 'transactions': transaction_list})



        student.wallet=(float)(student.wallet) + amount
        try:
            student.save()

            Transactions.objects.create(user=current_user, transaction_time=datetime.now(), added_amount=amount, subtracted_amount=0, details='Added money to wallet')

            messages.success(request,f'Successfully added PHP {amount_str} to your wallet!')
            return render(request, 'accounts/student_wallet.html', {'student': student, 'transactions': transaction_list})

        except:
            raise Http404("Oops! Could not add money. Please try again.")

    return render(request, 'accounts/student_wallet.html', {'student': student, 'transactions': transaction_list})

# def student_add_amount(request):
#     user = request.user
#
#     if 'amount' in request.POST:
#         wallet = user.wallet
#         wallet += request.POST.get('amount')
#         wallet.save()
#
#         trans = Transactions(user=user,
#                              transaction_time=datetime.now(),
#                              added_amount=request.POST.get('amount'),
#                              subtracted_amount=0,
#                              details=f'')
#
#
#         messages.success(request, f'Successfully added PHP {request.POST.get("amount")} to your wallet!')
#
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#     return render(request, 'accounts/student_wallet.html')

# @login_required
# def booking_session(request, id):
#     if request.method == 'POST':
#         tutor = TutorProfile.objects.get(user=id)
#         student = StudentProfile.objects.get(user=request.user)
#         subject = request.POST['Subject']
#         msg = request.POST['Message']
#         booking_instance = Bookings(student_id=student, tutor_id=tutor, subject=subject, student_msg=msg)
#         booking_instance.save()
#     else:
#         return HttpResponse('error')
#     return HttpResponse('Successfully booked')


class EmailThread(threading.Thread):
    """
    A thread to make email sending asynchronous
    """
    def __init__(self, subject, html_content, recipient_list, sender):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.sender, self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()


def send_html_mail(subject, html_content, recipient_list, sender):
    """
    Use this function to send an Email
    """
    EmailThread(subject, html_content, recipient_list, sender).start()


@login_required
def availability(request):
    if request.method == 'POST':
        form = TutorProfileForm(request.POST, instance=request.user.tutor_profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)

    else:

        form = TutorProfileForm(instance=request.user.tutor_profile)

    return render(request, 'accounts/availability.html', {'form': form})


@login_required
def tutor_application(request):
    if request.method == 'POST':
        profile_form = TutorProfileForm(request.POST, instance=request.user.tutor_profile)
        application_form = ApplicationForm(request.POST, request.FILES, instance=request.user.tutor_form)

        if profile_form.is_valid() and application_form.is_valid():
            profile_form.save()
            application_form.save()
            messages.success(request, f'Thank you for applying {request.user.first_name}! please wait while we review your application.')
            return HttpResponseRedirect('/')
    else:

        profile_form = TutorProfileForm(instance=request.user.tutor_profile)
        application_form = ApplicationForm(instance=request.user.tutor_form)

    context = {
        'profile_form': profile_form,
        'application_form': application_form
    }

    return render(request, 'accounts/application_view.html', context)


# class ApplicationView(LoginRequiredMixin, FormView):
#     template_name = 'accounts/application_view.html'
#     form_class = ApplicationForm
#     success_url = '/'
#
#     def form_valid(self, form):
#         tutor_application = form.save(commit=False)
#         tutor_application.tutor = self.request.user.tutor_profile
#         tutor_application.save()
#         first_name = form.cleaned_data.get('first_name')
#         messages.success(self.request, f'Thank you for applying {first_name}! please wait while we review your application.')
#         return HttpResponseRedirect(self.get_success_url())


class SignUpView(TemplateView):
    template_name = 'accounts/signup.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class BookingView(LoginRequiredMixin, CreateView):
    model = Bookings
    form_class = BookingsForm
    template_name = 'accounts/booking_view.html'
    success_url = '/'

    def form_valid(self, form):
        tutor = User.objects.get(id=self.kwargs.get('pk')) #get tutor in DetailView
        student = self.request.user.student_profile
        amount = tutor.tutor_profile.hourly_rate * int(form.cleaned_data['frequency'][0])

        if student.wallet < amount:
            messages.success(self.request, "You don't have enough balance for this session!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

        else:

            booking_form = form.save(commit=False)
            booking_form.student_id = student
            booking_form.tutor_id = tutor.tutor_profile

            subject = 'You have been Booked for a new session!'
            message = f'Dear{tutor.first_name}, You have been booked by {self.request.user.first_name}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [tutor.email]
            send_html_mail(subject,message,recipient_list,email_from)

            messages.success(self.request, f'You have successfully request a booking session with {tutor.first_name}')
            return super(BookingView, self).form_valid(form)


class TutorBookedSession(LoginRequiredMixin, ListView):
    """
    tutor booked request
    """
    model = Bookings
    template_name = 'accounts/tutor_booked_request.html'
    context_object_name = 'bookings'
    paginate_by = 7


class ActiveSession(LoginRequiredMixin, ListView):
    model = Bookings
    template_name = 'accounts/booked_session.html'
    context_object_name = 'active_sessions'
    ordering = ['-id']

    """
    handle two context object at the same time
    """
    def get_context_data(self,  **kwargs):
        context = super(ActiveSession, self).get_context_data(**kwargs)
        context['rooms'] = Classroom.objects.all()
        return context

    def get_queryset(self):
        if self.request.user.is_tutor:
            tutor_profile = self.request.user.tutor_profile
            filter_bookings = Bookings.objects.filter(tutor_id=tutor_profile, on_session=True)
            return filter_bookings

        if self.request.user.is_student:
            student_profile = self.request.user.student_profile
            filter_bookings = Bookings.objects.filter(student_id=student_profile, on_session=True)
            return filter_bookings


@login_required
def end_session(request, id):
    session = Bookings.objects.get(id=id)

    if request.method == 'POST':
        if request.user.is_tutor:
            student = session.student_id.user
            tutor = request.user
            tutor_has_bookings = len(Bookings.objects.filter(tutor_id=tutor.tutor_profile))
            student_has_bookings = len(Bookings.objects.filter(student_id=student.student_profile))

            subject = 'Session ended'
            message = f'Your session with {tutor.first_name} has now ended. Thank you for choosing gurufinder!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [student.email]
            send_html_mail(subject, message, recipient_list, email_from)

            session.delete()

            if student_has_bookings >=2 and tutor_has_bookings < 2:
                tutor.tutor_profile.has_bookings = False
                tutor.save()

                return HttpResponseRedirect(reverse('accounts:end_session_rating_student', kwargs={'id': session.student_id.id}))


            elif tutor_has_bookings >=2 and student_has_bookings < 2:
                student.student_profile.has_bookings = False
                student.save()

                return HttpResponseRedirect(reverse('accounts:end_session_rating_student', kwargs={'id': session.student_id.id}))

            else:

                student.student_profile.has_bookings = False
                tutor.tutor_profile.has_bookings = False
                tutor.save()
                student.save()

                return HttpResponseRedirect(reverse('accounts:end_session_rating_student', kwargs={'id': session.student_id.id}))

            return HttpResponseRedirect(reverse('accounts:end_session_rating_student', kwargs={'id': session.student_id.id}))


        elif request.user.is_student:
            student = request.user
            tutor = session.tutor_id.user
            tutor_has_bookings = len(Bookings.objects.all().filter(tutor_id=tutor.tutor_profile))
            student_has_bookings = len(Bookings.objects.all().filter(student_id=student.student_profile))

            subject = 'Session ended'
            message = f'Your session with {student.first_name} has now ended. Thank you!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [tutor.email]
            send_html_mail(subject, message, recipient_list, email_from)

            session.delete()

            if student_has_bookings >= 2  and tutor_has_bookings < 2:
                tutor.tutor_profile.has_bookings = False
                tutor.save()

                return HttpResponseRedirect(reverse('accounts:end_session_rating_tutor', kwargs={'id': session.tutor_id.id}))


            elif tutor_has_bookings >= 2 and student_has_bookings < 2:
                student.student_profile.has_bookings = False
                student.save()

                return HttpResponseRedirect(reverse('accounts:end_session_rating_tutor', kwargs={'id': session.tutor_id.id}))


            else:

                student.student_profile.has_bookings = False
                tutor.tutor_profile.has_bookings = False
                tutor.save()
                student.save()

                return HttpResponseRedirect(reverse('accounts:end_session_rating_tutor', kwargs={'id': session.tutor_id.id}))

            return HttpResponseRedirect(reverse('accounts:end_session_rating_tutor', kwargs={'id': session.tutor_id.id}))

    return render(request, 'accounts/session_cancel.html')


def end_session_rating_student(request, id):
    obj_student = get_object_or_404(StudentProfile, id=id)

    student = StudentProfile.objects.filter(id=id)

    context = {
        'student_end_session':student,
        'student_name':obj_student.user.first_name
               }

    return render(request, 'accounts/end_session_rating.html', context)

def end_session_rating_tutor(request, id):
    obj_tutor = get_object_or_404(TutorProfile, id=id)

    tutor = TutorProfile.objects.filter(id=id)

    context = {
        'tutor_end_session':tutor,
        'tutor_name':obj_tutor.user.first_name
               }

    return render(request, 'accounts/end_session_rating_tutor.html', context)


@login_required
def deny_request(request, id):

    obj = get_object_or_404(Bookings, id=id)

    if request.method == 'POST':
        form = DenyRequestForm(request.POST)

        if form.is_valid():
            subject = f'Sorry, but your request for booking with {request.user.first_name} has been denied'
            message = f"{request.user.first_name}'s message: {form.cleaned_data['deny_msg']}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [obj.student_id.user.email]
            send_html_mail(subject,message,recipient_list,email_from)
            obj.delete()

            return redirect('accounts:tutor_bookings')
    else:

        context = {
            'form': DenyRequestForm(request.POST)
        }

    return render(request, 'accounts/deny_request.html', context)


@login_required
def accept_request(request, id):
    obj = Bookings.objects.get(id=id) #get the id of a booking instance
    student = obj.student_id.user
    tutor = request.user
    session = obj
    lang_description = {'Python': 'Python is an interpreted high-level general-purpose programming language.',
                        'JavaScript': 'JavaScript, often abbreviated as JS, is a programming language that conforms to the ECMAScript specification.',
                        'PHP': 'PHP is a general-purpose scripting language geared towards web development.',
                        'Java': 'Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible.',
                        'C#': 'C# is a general-purpose, multi-paradigm programming language encompassing static typing, strong typing, lexically scoped, imperative, declarative, functional, generic, object-oriented, and component-oriented programming disciplines.',
                        'Sql': 'SQL is a domain-specific language used in programming and designed for managing data held in a relational database management system.',
                        'Swift': 'Swift is a general - purpose, multi - paradigm, compiled programmin language developed by Apple Inc. and the open - source community.'
                        }

    if request.method == 'POST':
        subject = 'Accepted'
        message = f'You have successfully booked a session with {tutor.first_name}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [student.email]
        send_html_mail(subject,message,recipient_list,email_from)

        tutor.tutor_profile.has_bookings = True
        student.student_profile.has_bookings = True
        session.on_session = True
        session.start_time = datetime.now()
        session.end_time = datetime.now()
        print(tutor)

        if tutor.tutor_profile.students == None:
            tutor.tutor_profile.students = [student.username]
            tutor.save()
        elif tutor.tutor_profile.students and student.username not in tutor.tutor_profile.students :
            tutor.tutor_profile.students.append(student.username)
            tutor.save()
            #assign as one of the tutors student

        session.save()
        student.save()

        if int(session.frequency[0]) <= 0:
            session_frequency = tutor.tutor_profile.hourly_rate
        else:
            session_frequency = tutor.tutor_profile.hourly_rate * int(session.frequency[0])

        student.student_profile.wallet -= session_frequency
        student.save()

        tutor.tutor_profile.wallet += session_frequency
        tutor.save()

        check_frequency_student = {
            0:f'Booked a Session with {tutor.first_name.title()} for {student.first_name.title()}'
        }

        var1 = f'Booked {session.frequency[0]} Session with {tutor.first_name.title()} for {student.first_name.title()}'

        transaction_student = Transactions.objects.create(user=student, transaction_time=datetime.now(), added_amount=0, subtracted_amount=session_frequency, details=f"{check_frequency_student.get(int(session.frequency[0]), var1)}")

        transaction_tutor = Transactions.objects.create(user=tutor, transaction_time=datetime.now(
        ), added_amount=session_frequency, subtracted_amount=0, details=f'Received Payment for Session with {student.first_name.title()}')

        """
        create instance of classroom
        """
        classroom = Classroom(bookings=obj,
                              name=f'({obj.id}) {tutor.first_name.capitalize()} {tutor.last_name.capitalize()}',
                              description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quasi voluptat hic provident nulla repellat facere esse molestiae ipsa labore porro minima quam quaerat rem, natus repudiandae debitis est sit pariatur.",
                              )
                              # description=f'{obj.subject} class')
        classroom.save()

        """
        create instance of subject and assign to classroom
        """
        questions = Question.objects.all()
        subject_ins = Subject.objects.create(subject_id=f'({obj.id}) {obj.subject}',
                              name=f'{obj.subject}',
                              classroom=Classroom.objects.get(id=classroom.id),
                              image=ImageFile(open(f'media/{obj.subject}.png', 'rb')),
                              description=lang_description.get(obj.subject)
                              )

        subject_ins.questions.add(*questions)
        subject_ins.save()

        if int(session.frequency) == 0:
            session.end_time += timedelta(hours=1)  # due
            session.save()
        else:
            session.end_time += timedelta(hours=int(session.frequency))  # due
            session.save()

        print(session.frequency)
        print(session.end_time)


        if session.subject == 'Python':
            create_lesson(request.user, obj.subject, classroom, session.id, subject_ins.id)
        if session.subject == 'JavaScript':
            create_lesson(request.user, obj.subject, classroom, session.id, subject_ins.id)


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'accounts/tutor_booked_request.html')


class StudentSignUpView(FormView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/signup_form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        messages.success(self.request, 'Please confirm your email.')
        return_val = super(StudentSignUpView, self).form_valid(form)
        send_email(user)
        return return_val


class TutorSignUpView(FormView):
    model = User
    form_class = TutorSignUpForm
    template_name = 'accounts/signup_form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tutor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        messages.success(self.request, 'Please confirm your email.')
        return_val = super(TutorSignUpView, self).form_valid(form)
        send_email(user)
        return return_val


# class TutorListView(LoginRequiredMixin, ListView):
#     model = User
#     template_name = 'accounts/tutor_list.html'
#     context_object_name = 'tutors'
#     paginate_by = 7


class TutorListView(LoginRequiredMixin, ListView):
    model = TutorProfile
    template_name = 'accounts/tutor_list.html'
    context_object_name = 'tutors'
    ordering = ['-tutor_ratings__average']
    paginate_by = 6


class SearchTutorLanguage(ListView):
    model = TutorProfile
    template_name = 'accounts/tutor_list.html'
    context_object_name = 'tutors'
    paginate_by = 5

    def get_queryset(self):
        query1 = self.request.GET.get('language')
        query2 = self.request.GET.get('availability')
        return TutorProfile.objects.filter(programming_languages__icontains=query1, availability__icontains=query2).order_by('-tutor_ratings__average')


class TutorDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'accounts/tutor_detail_view.html'
    context_object_name = 'tutor_detail'

# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserUpdateForm
#     second_form_class = TutorProfileForm
#     template_name = 'accounts/profile_update.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileUpdateView, self).get_context_data(**kwargs)
#
#         if 'form' not in context:
#             context['form'] = self.form_class(self.request.GET)
#         if 'form2' not in context:
#             context['form2'] = self.second_form_class(self.request.GET)
#         return context
#
#     def get(self, request, *args, **kwargs):
#         super(ProfileUpdateView, self).get(request, *args, **kwargs)
#         form = self.form_class
#         form2 = self.second_form_class
#         return self.render_to_response(self.get_context_data(object=self.object, form=form, form2=form2))
#
#     def get_success_url(self):
#         self.object = self.get_object()
#         return reverse_lazy('accounts:profile')
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.form_class(request.POST)
#         form2 = self.second_form_class(request.POST)
#
#         if form.is_valid() and form2.is_valid():
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(self.get_context_data(form=form, form2=form2))
#
#     def get_object(self, *args, **kwargs):
#         return User.objects.get(username=self.kwargs.get('username'))
#
#     def get_success_url(self):
#         self.object = self.get_object()
#         return reverse_lazy('accounts:profile_update', self.request.user.username)


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
     model = User
     form_class = UserUpdateForm
     template_name = 'accounts/profile_update.html'

     def get_object(self, *args, **kwargs):
         return User.objects.get(username=self.kwargs.get('username'))

     def get_success_url(self):
         self.object = self.get_object()
         return reverse_lazy('accounts:profile_update', self.request.user.username)

     def get_form_kwargs(self):
         form = super().get_form_kwargs()
         form['user'] = self.request.user
         return form


@admin.register(Application)
class Application(admin.ModelAdmin):
    """
    accept or deny a tutor application in admin site
    """
    list_display = ['user', 'approved', 'confirmed', 'denied']

    def confirmed(self, obj):
        url = reverse('admin:confirm_url', kwargs={'id': obj.id})
        self.object = self.get_object(self, obj.id)
        tutor = self.object.user.tutor_profile.is_validated
        if not tutor:
            return format_html('<a class="button" href="{}">Confirm</a>', url)

    def denied(self, obj):
        url = reverse('admin:denied_url', kwargs={'id': obj.id})
        self.object = self.get_object(self, obj.id)
        tutor = self.object.user.tutor_profile.is_validated
        if not tutor:
            return format_html('<a class="button" href="{}">Deny</a>', url)

    def approved(self, obj):
        self.object = self.get_object(self, obj.id)
        return f'{self.object.user.tutor_profile.is_validated}'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('confirm/<int:id>', self.confirmed_application, name='confirm_url'),
            path('deny/<int:id>', self.denied_application, name='denied_url'),
            path('validated/<int:id>', self.approved_application, name='approved_url'),
        ]
        return custom_urls + urls

    def confirmed_application(self, request, id):
        self.object = self.get_object(request, id) #get tutor application id

        subject = 'Approved'
        message = f'Your application has been approved.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.object.user.email]
        send_html_mail(subject, message, recipient_list, email_from)

        tutor = self.object.user.tutor_profile
        tutor.is_validated = True
        tutor.save()

        redirect_url = "admin:{}_{}_changelist".format(self.opts.app_label, self.opts.model_name)
        return redirect(reverse(redirect_url))

    def denied_application(self, request, id):
        self.object = self.get_object(request, id)

        subject = 'Rejected'
        message = f'Your application has been denied.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.object.user.email]
        send_html_mail(subject, message, recipient_list, email_from)

        redirect_url = f"admin:{self.opts.app_label}_{self.opts.model_name}_changelist"
        return redirect(reverse(redirect_url))

    def approved_application(self, request, id):
        redirect_url = f"admin:{self.opts.app_label}_{self.opts.model_name}_changelist"
        return redirect(reverse(redirect_url))


def create_lesson(user, subject, classroom, booking_id, subject_id):
    if subject == 'Python':
        python(user, subject, classroom, booking_id, subject_id)
    elif subject == 'JavaScript':
        javascript(user, subject, classroom, booking_id, subject_id)


def python(user, subject, classroom, booking_id, subject_id):
    lesson1 = Lesson(lesson_id=f'{booking_id}-{subject} setup',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Python Setup',
                     position=1,
                     slug=f'{booking_id}-python-setup',
                     video=File(open('media/intro_vid.mp4', 'rb'))
                     )
    lesson1.save()

    lesson2 = Lesson(lesson_id=f'{booking_id}-{subject} object and data structure',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Python Object and Data Structure',
                        position=2,
                        slug=f'{booking_id}-python-object-and-data-structure',
                     )
    lesson2.save()

    lesson3 = Lesson(lesson_id=f'{booking_id}-{subject} comparison operators',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Python Comparison Operators',
                        position=3,
                        slug=f'{booking_id}-python-comparison-operators',
                     )
    lesson3.save()

    lesson4 = Lesson(lesson_id=f'{booking_id}-{subject} statements',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Python Statements',
                        position=4,
                        slug=f'{booking_id}-python-statements',
                    )
    lesson4.save()

    lesson5 = Lesson(lesson_id=f'{booking_id}-method and functions',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Method and Functions',
                        position=5,
                        slug=f'{booking_id}-method-and-functions',
                     )
    lesson5.save()

    lesson6 = Lesson(lesson_id=f'{booking_id}-modules and packages',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Modules and Packages',
                        position=6,
                        slug=f'{booking_id}-modules-and-packages',
                     )
    lesson6.save()

    lesson7= Lesson(lesson_id=f'{booking_id}-errors and exception handling',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Errors and Exception Handling',
                        position=7,
                        slug=f'{booking_id}-errors-and-exception-handling',
                    )
    lesson7.save()

    lesson8 = Lesson(lesson_id=f'{booking_id}-object oriented programming',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Object Oriented Programming',
                        position=8,
                        slug=f'{booking_id}-object-oriented-programming',
                     )
    lesson8.save()

    lesson9 = Lesson(lesson_id=f'{booking_id}-{subject} decoratos',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Python Decorators',
                        position=9,
                        slug=f'{booking_id}-python-decorators',
                     )
    lesson9.save()

    lesson10 = Lesson(lesson_id=f'{booking_id}-{subject} generators',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Python Generators',
                        position=10,
                        slug=f'{booking_id}-python-generators',
                      )
    lesson10.save()

    lesson11 = Lesson(lesson_id=f'{booking_id}-advance {subject} modules',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Advance Python Modules',
                        position=11,
                        slug=f'{booking_id}-advace-python-modules',
                      )
    lesson11.save()

    lesson12 = Lesson(lesson_id=f'{booking_id}-advance {subject} objects and data structures',
                        Classroom=Classroom.objects.get(id=classroom.id),
                        created_by=user,
                        subject=Subject.objects.get(id=subject_id),
                        name=f'Advance Python Objects and Data Structures',
                        position=12,
                        slug=f'{booking_id}-advance-python-objects-and-data-structures',
                      )
    lesson12.save()

def javascript(user, subject, classroom, booking_id, subject_id):
    lesson1 = Lesson(lesson_id=f'{booking_id}-{subject} fundamentals',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'JavaScript Fundamentals',
                     position=1,
                     slug=f'{booking_id}-javaScript-fundamentals',
                     video=File(open('media/intro_vid.mp4', 'rb'))
                     )
    lesson1.save()

    lesson2 = Lesson(lesson_id=f'{booking_id}-objects: the basics',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Objects: the basics',
                     position=2,
                     slug=f'{booking_id}-objects-the-basics',
                     )
    lesson2.save()

    lesson3 = Lesson(lesson_id=f'{booking_id}-data types',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Data Types',
                     position=3,
                     slug=f'{booking_id}-data-types',
                     )
    lesson3.save()

    lesson4 = Lesson(lesson_id=f'{booking_id}-advance working with functions',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Advance Working With Functions',
                     position=4,
                     slug=f'{booking_id}-advance-working-with-functions',
                     )
    lesson4.save()

    lesson5 = Lesson(lesson_id=f'{booking_id}-object properties configuration',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Object Properties Configuration',
                     position=5,
                     slug=f'{booking_id}-object-properties-configuration',
                     )
    lesson5.save()

    lesson6 = Lesson(lesson_id=f'{booking_id}-prototypes and inheritance',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Prototypes and Inheritance',
                     position=6,
                     slug=f'{booking_id}-prototypes-and-inheritance',
                     )
    lesson6.save()

    lesson7 = Lesson(lesson_id=f'{booking_id}-{subject} classes',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'JavaScript Classes',
                     position=7,
                     slug=f'{booking_id}-javascript-classes',
                     )
    lesson7.save()

    lesson8 = Lesson(lesson_id=f'{booking_id}-promises and async/await',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Promises and Async/Await',
                     position=8,
                     slug=f'{booking_id}-promises-and-async-await',
                     )
    lesson8.save()

    lesson9 = Lesson(lesson_id=f'{booking_id}-generators and advanced iteration',
                     Classroom=Classroom.objects.get(id=classroom.id),
                     created_by=user,
                     subject=Subject.objects.get(id=subject_id),
                     name=f'Generators and Advanced Iteration',
                     position=9,
                     slug=f'{booking_id}-generators-and-advanced-iteration',
                     )
    lesson9.save()