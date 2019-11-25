from django.urls import path
from . import views
from .views import *
from users.views import profile

urlpatterns = [
    path('', QuestionListView.as_view(), name='blog-home'),
    path('quizzes/', QuizListView.as_view(), name='quiz-papers'),
    path('quizSelect/', views.select_quiz, name='quiz-select'),
    path('remove/', views.remove_from_quiz, name='remove'),
    path('searchQuestions/', SearchableQuestionListView.as_view(), name='question-search'),
    path('searchQuestionModules/', SearchableQuestionModuleListView.as_view() , name='module-search'),
    path('export/', views.export , name="export"),
    path('quiz/', views.pdf_view, name="quiz-download"),
    path('download/', views.download, name='download'),
    path('qb/',views.pdf_view2, name="qb-download"),
    path('qb-upload/', views.upload_qbfiles, name='qb-upload'),


    path('post/new/', QuestionCreateView.as_view(), name='post-create'),
    path('post/newQuiz/', QuizCreateView.as_view(), name='quiz-create'),
    path('post/newQuestionViaFile/', views.add_question, name='qvf-create'),
    path('post/newBank/', QuestionBankCreateView.as_view(), name='bank-create'),
    path('post/newModule/', QuestionModuleCreateView.as_view(), name='module-create'),
    path('post/newFile/', views.upload_files, name='upload-file'),

    path('post/<int:pk>/', QuestionDetailView.as_view(), name='post-detail'),
    path('post/qb/<int:pk>/', QuestionBankDetailView.as_view(), name='bank-detail'),
    path('post/qm/<int:pk>/', QuestionModuleDetailView.as_view(), name='module-detail'),
    path('post/qp/qb/<int:pk>/', QuestionDetailViewQuiz.as_view(), name='postQuiz-detail'),
    path('post/qp/qm/<int:pk>/', QuestionModuleDetailViewQuiz.as_view(), name='moduleQuiz-detail'),
    path('post/qp/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),


    path('post/<int:pk>/update/', QuestionUpdateView.as_view(), name='post-update'),
    path('post/qb/<int:pk>/update/', QuestionBankUpdateView.as_view(), name='bank-update'),
    path('post/qm/<int:pk>/update/', QuestionModuleUpdateView.as_view(), name='module-update'),
    path('post/qp/<int:pk>/update/', QuizUpdateView.as_view(), name='quiz-update'),

    path('post/<int:pk>/delete/', QuestionDeleteView.as_view(), name="post-delete"),
    path('post/qb/<int:pk>/delete/', QuestionBankDeleteView.as_view(), name="bank-delete"),
    path('post/qm/<int:pk>/delete/', QuestionModuleDeleteView.as_view(), name="module-delete"),
    path('post/qp/<int:pk>/delete/', QuizDeleteView.as_view(), name="quiz-delete"),

    path('about/', views.about, name='blog-about'),
]