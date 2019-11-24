import django_filters
from .models import Question, QuestionModule
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class QuestionFilter(django_filters.FilterSet):


    class Meta:
        model = Question
        fields = {
            'statement': ['icontains'],
            'marks': ['gt', 'lt', 'exact'],
            'chapter_tag': ['icontains'],
            'section_tag': ['icontains']
        }


class QuestionModuleFilter(django_filters.FilterSet):
    # date_posted = django_filters.DateTimeFilter(
    #     widget=DateInput(
    #         attrs={
    #             'class': 'datepicker'
    #         }
    #     ),
    #     lookup_expr='exact'
    # )

    class Meta:
        model = QuestionModule
        fields = {
            'statement': ['icontains'],
            'marks': ['gt', 'lt', 'exact'],
        }