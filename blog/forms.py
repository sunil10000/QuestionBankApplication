from django import forms
from .models import UploadedFile,Question


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


class AddQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['statement', 'answer', 'marks', 'difficulty', 'tags', 'parent', 'isRoot']