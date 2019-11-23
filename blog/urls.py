from django.urls import path
from . import views
from .views import *
from users.views import profile

urlpatterns = [
    path('', QuestionListView.as_view(), name='blog-home'),



    path('post/new/', QuestionCreateView.as_view(), name='post-create'),
    path('post/newQuestionViaFile/', views.add_question, name='qvf-create'),
    path('post/newBank/', QuestionBankCreateView.as_view(), name='bank-create'),
    path('post/newModule/', QuestionModuleCreateView.as_view(), name='module-create'),
    path('post/newFile/', views.upload_files, name='upload-file'),

    path('post/<int:pk>/', QuestionDetailView.as_view(), name='post-detail'),
    path('post/qb/<int:pk>/', QuestionBankDetailView.as_view(), name='bank-detail'),
    path('post/qm/<int:pk>/', QuestionModuleDetailView.as_view(), name='module-detail'),


    path('post/<int:pk>/update/', QuestionUpdateView.as_view(), name='post-update'),
    path('post/qb/<int:pk>/update/', QuestionBankUpdateView.as_view(), name='bank-update'),
    path('post/qm/<int:pk>/update/', QuestionModuleUpdateView.as_view(), name='module-update'),

    path('post/<int:pk>/delete/', QuestionDeleteView.as_view(), name="post-delete"),
    path('post/qb/<int:pk>/delete/', QuestionBankDeleteView.as_view(), name="bank-delete"),
    path('post/qm/<int:pk>/delete/', QuestionModuleDeleteView.as_view(), name="module-delete"),

    path('about/', views.about, name='blog-about'),
]