from django.urls import path
from . import views
from .views import (
    QuestionListView,
    QuestionDetailView,
    QuestionUpdateView,
    QuestionCreateView,
    QuestionDeleteView
)
from users.views import profile

urlpatterns = [
    path('', QuestionListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', QuestionDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', QuestionUpdateView.as_view(), name='post-update'),
    path('post/new/', QuestionCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/delete/', QuestionDeleteView.as_view(), name="post-delete"),
]