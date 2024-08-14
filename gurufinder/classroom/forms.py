from django import forms
from .models import Comment, Reply, Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_id', 'name', 'position', 'video', 'ppt', 'Notes']


# class LessonCompleted(forms.ModelForm):
#     class Meta:
#         model = Lesson
#         fields = ['completed']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        labels = {'body': 'comment'}

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 70, 'placeholder': "Enter Your Comment"}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_body']

        widgets = {
            'reply_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 10})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReplyForm, self).__init__(*args, **kwargs)