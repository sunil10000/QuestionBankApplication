from django.shortcuts import render,redirect
from .models import QuestionBank
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView


def home(request):
    context={
        'questionBank': QuestionBank.objects.all(),
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)


class QuestionListView(ListView):
    model = QuestionBank
    template_name = 'blog/home.html' #<app>/<model>_<ListView>.html
    context_object_name = 'posts'
    ordering = ['date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Home"
        return context


class QuestionDetailView(DetailView):
    model = QuestionBank
    template_name = 'blog/questionbank_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Details"
        return context


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = QuestionBank
    fields = ['title', 'file_field']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        # request = self.request
        # if request.method == "POST":
        #     form.instance.author = request.user
        #     form.save()
        #     return redirect('blog-home')
        # else:
        #     return render(request, 'blog/questionbank_form.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create new post"
        return context


class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = QuestionBank
    fields = ['title', 'file_field']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Post"
        return context


class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = QuestionBank
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Post"
        return context


def about(request):
    context = {
        'title':"About"
    }
    return render(request, 'blog/about.html',context)


# def upload(request):
#     if request.method == "POST":
#         uploaded_file = request.FILES['questionPaper']
#         print(uploaded_file.name)
#         print(uploaded_file.size)
#         fs = FileSystemStorage()
#         fs.save(uploaded_file.name, uploaded_file)
#         return redirect('blog-home')
#     else:
#         return render(request, 'blog/questionbank_form.html')

