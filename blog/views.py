from django.shortcuts import render,redirect
from .models import Question,QuestionBank,QuestionModule
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView


# def home(request):
#     context={
#         'questionBanks': QuestionBank.objects.all(),
#         'title': 'Home'
#     }
#     return render(request, 'blog/home.html', context)


class QuestionListView(ListView):
    model = QuestionBank
    template_name = 'blog/home.html' #<app>/<model>_<ListView>.html
    context_object_name = 'questionBanks'
    ordering = ['date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Home"
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
#         return render(request, 'blog/question_form.html')


class QuestionBankCreateView(LoginRequiredMixin, CreateView):
    model = QuestionBank
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create new question bank"
        return context


class QuestionModuleCreateView(LoginRequiredMixin, CreateView):
    model = QuestionModule
    fields = ['statement', 'parent', 'isRoot']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.marks = 0
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create new question Module"
        return context


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    fields = ['statement', 'answer', 'marks', 'difficulty', 'tags', 'parent', 'isRoot']

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create new post"
        return context


class QuestionBankDetailView(DetailView):
    model = QuestionBank
    template_name = 'blog/questionbank_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Bank Details"
        context['qs'] = Question.objects.all()
        context['qms'] = QuestionModule.objects.all()
        return context


class QuestionModuleDetailView(DetailView):
    model = QuestionModule
    template_name = 'blog/questionmodule_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Module Details"
        context['qs'] = Question.objects.all()
        context['qms'] = QuestionModule.objects.all()
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'blog/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Details"
        return context


class QuestionBankUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = QuestionBank
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Question Bank"
        return context


class QuestionModuleUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = QuestionModule
    fields = ['statement']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Question Module"
        return context


class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Question
    fields = ['statement', 'answer', 'marks', 'difficulty', 'tags']

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


class QuestionModuleDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = QuestionModule
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Post"
        context['qs'] = Question.objects.all()
        context['qms'] = QuestionModule.objects.all()
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        id = self.object.parent
        delete_module(id)
        self.object.delete()
        return redirect(success_url)


class QuestionBankDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = QuestionBank
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Post"

        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        id = self.object.parent
        delete_bank(id)
        self.object.delete()
        return redirect(success_url)


class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Question
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Post"
        return context


def delete_bank(id):
    Question.objects.get(parent=id, isRoot=1).delete()
    qms = QuestionModule.objects.get(parent=id, isRoot=1)
    for qm in qms:
        delete_module(qm.id)
    qms.delete()


def delete_module(id):
    qus = Question.objects.filter(parent=id, isRoot=0)
    for q in qus:
        q.delete()
    qms = QuestionModule.objects.filter(parent=id, isRoot=0)
    for qm in qms:
        delete_module(qm.id)
    qms.delete()
