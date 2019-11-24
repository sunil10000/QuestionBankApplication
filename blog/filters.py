import django_filters
from .models import Question, QuestionModule


class QuestionFilter(django_filters.FilterSet):

    class Meta:
        model = Question
        fields = {
            'statement': ['icontains'],
            'marks': ['gt'],
            'difficulty': [],
        }
        #     'tags' : ['icontains'],}
        #     'difficulty'
        #     'date_posted'
        # }


class QuestionModuleFilter(django_filters.FilterSet):

    class Meta:
        model = QuestionModule
        fields = ('marks', 'date_posted')
