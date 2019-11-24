from django import forms
from .models import UploadedFile,Question,JustToChose


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'parent', 'isRoot']


class AddQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['statement', 'answer', 'marks', 'difficulty', 'chapter_tag', 'parent', 'isRoot']


class ChoseDrowDown(forms.Form):
    option = forms.ChoiceField()
    qid = forms.CharField()
    isQ = forms.CharField()


class RemoveForm(forms.Form):
    qid = forms.CharField()
    quiz_id = forms.CharField()
    isQ = forms.CharField()


class ExportForm(forms.Form):
    title = forms.CharField()
    top_border_in_inchs = forms.DecimalField(max_digits=2)
    bottom_border_in_inchs = forms.DecimalField(max_digits=2)
    left_border_in_inchs = forms.DecimalField(max_digits=2)
    right_border_in_inchs = forms.DecimalField(max_digits=2)
    quiz_id = forms.IntegerField()


class DownloadForm(forms.Form):
    qbid = forms.IntegerField()


