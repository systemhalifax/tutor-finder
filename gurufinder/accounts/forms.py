from django.contrib.auth.forms import UserCreationForm
from .models import User, Application, TutorProfile, Bookings
from django import forms


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'current_address', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user


class TutorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'current_address', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_tutor = True
        if commit:
            user.save()
        return user


class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['profile_headline', 'hourly_rate', 'bio', 'availability', 'programming_languages']

        labels = {'profile_headline': 'Profile Headline'}

        widgets = {
            'bio': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'cols': 70}),
        }

class UserUpdateForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['phone_number'].initial = user.phone_number
        self.fields['current_address'].initial = user.current_address
        self.fields['image'].initial = user.image

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'current_address', 'image']

    # def __init__(self, *args, **kwargs):
    #     super(UserUpdateForm, self).__init__(*args, **kwargs)
    #     self.fields['first_name'].required = False
    #     self.fields['last_name'].required = False
    #     self.fields['email'].required = False
    #     self.fields['phone_number'].required = False
    #     self.fields['current_address'].required = False





class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['valid_id', 'selfie', 'portfolio']

        labels = {'valid_id': "Upload a Valid ID",
                  'selfie': 'Upload photo of yourself',
                  'portfolio': 'Upload your portfolio as a zip file'}


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['profile_headline', 'bio', 'availability', 'programming_languages']

        labels = {'profile_headline': 'Profile Headline'}

        widgets = {
            'bio': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'cols': 70}),
        }


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['subject', 'frequency', 'student_msg']

        labels = {'student_msg': 'Message'}


#for bookings model
class DenyRequestForm(forms.Form):
    deny_msg = forms.CharField(widget=forms.Textarea, max_length=100, required=False, label='Message to student')



 # #Fix TypeError: __init__() got an unexpected keyword argument 'request'
 # def __init__(self, *args, **kwargs):
 #    self.request = kwargs.pop('request', None)
 #     super(ApplicationForm, self).__init__(*args, **kwargs)


# class TutorUpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'current_address', 'bio']
#
#         labels = {'first_name':'first name',
#                   'last_name': 'last name',
#                   'emai':'email',
#                   'phone_number':'phone number',
#                   'current_address':'current address',
#                   'bio':'bio'}