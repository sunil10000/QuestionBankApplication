from django.shortcuts import render,redirect
from .models import Question,QuestionBank,QuestionModule, UploadedFile, QuizPaper
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.forms.models import model_to_dict
from .forms import AddQuestion,FileUploadForm,ChoseDrowDown,RemoveForm
import configparser
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.core.files.base import ContentFile



# def home(request):
#     context={
#         'questionBanks': QuestionBank.objects.all(),
#         'title': 'Home'
#     }
#     return render(request, 'blog/home.html', context)

def remove_from_quiz(request):
    form = RemoveForm()
    if request.method == "POST":
        form = RemoveForm(request.POST)
        if form.is_valid():
            quiz_id = form.cleaned_data['quiz_id']
            q_id = form.cleaned_data['qid']
            is_Q = form.cleaned_data['isQ']
            if is_Q == '1':
                quiz = QuizPaper.objects.get(pk=quiz_id)
                qid_list = quiz.qid_list.split(",")
                qid_list = set(qid_list)
                qid_list.remove(q_id)
                qid_list = list(qid_list)
                qid_list = ",".join(qid_list)
                quiz.qid_list = qid_list
                quiz.save()
            else:
                quiz = QuizPaper.objects.get(pk=quiz_id)
                qmid_list = quiz.qmid_list.split(",")
                qmid_list = set(qmid_list)
                qmid_list.remove(q_id)
                qmid_list = list(qmid_list)
                qmid_list = ",".join(qmid_list)
                quiz.qmid_list = qmid_list
                quiz.save()
            return redirect("quiz-detail", pk=quiz_id)
        else:
            return render(request, "blog/remove.html", {'form': form})
    else:
        return render(request, "blog/remove.html", {'form': form})


def select_quiz(request):
    form = ChoseDrowDown()
    if request.method == "POST":
        form = ChoseDrowDown(request.POST)
        tup_list = QuizPaper.objects.values_list('title', 'id')
        tup_list = [('{0}:{1}'.format(p[0], p[1]), '{0}:{1}'.format(p[0], p[1])) for p in tup_list]
        form.fields['option'].choices = tup_list
        form.fields['option'].initial = tup_list[0]
        if form.is_valid():
            answer = form.cleaned_data['option']
            quiz_id = answer.split(":")[1]
            q_id = form.cleaned_data['qid']
            is_Q = form.cleaned_data['isQ']
            if is_Q == '1':
                quiz = QuizPaper.objects.get(pk=quiz_id)
                qid_list = quiz.qid_list.split(",")
                qid_list = set(qid_list)
                qid_list.add(q_id)
                qid_list = list(qid_list)
                qid_list = ",".join(qid_list)
                quiz.qid_list = qid_list
                quiz.save()
                return redirect('post-detail', q_id)
            else:
                quiz = QuizPaper.objects.get(pk=quiz_id)
                quiz.qmid_list += "," + str(q_id)
                qmid_list = quiz.qmid_list.split(",")
                qmid_list = set(qmid_list)
                qmid_list.add(q_id)
                qmid_list = list(qmid_list)
                qmid_list = ",".join(qmid_list)
                quiz.qid_list = qmid_list
                quiz.save()
                return redirect('module-detail', q_id)
        else:
            return render(request, "blog/select_quiz.html", {'form': form})
    else:
        tup_list = QuizPaper.objects.values_list('title', 'id')
        # for id,title in zip(quiz_ids,quiz_titles):
        #     tup_list.append((id, title))
        tup_list = [('{0}:{1}'.format(p[0], p[1]),'{0}:{1}'.format(p[0], p[1])) for p in tup_list]
        form.fields['option'].choices = tup_list
        form.fields['option'].initial = tup_list[0]
        print(form.fields['option'].choices)
        return render(request, "blog/select_quiz.html", {'form': form})


def handle_uploaded_file(myfile):
    config = configparser.ConfigParser()
    file_path = "media/QuestionFiles/"+myfile.name
    config.read(file_path)
    os.remove(file_path)
    UploadedFile.objects.all().delete()
    dictionary = []
    for section in config.sections():
        mydict = {}
        for option in config.options(section):
            mydict[option] = config.get(section, option)
        dictionary.append(mydict)
    print(dictionary)
    return dictionary


def add_question(request, *args, **kwargs):
    mydict = request.session.get('mydict')
    parent = request.session.get('parent')
    isRoot = request.session.get('isRoot')
    print("hi")
    print(isRoot)
    if request.method == 'POST':
        question_form = AddQuestion(request.POST, request.FILES)
        if question_form.is_valid():
            question_form.instance.author = request.user
            question_form.save()
            request.session['mydict'] = mydict[1:]
            return redirect(add_question)
        else:
            return render(request, "blog/question_form2.html", {'form': question_form, 'mydict': mydict, 'isRoot': isRoot, 'parent':parent})
    else:
        if len(mydict) == 0:
            print("again")
            print(isRoot)
            if isRoot == "1":
                return redirect("bank-detail", pk=parent)
            else:
                return redirect("module-detail", pk=parent)
        else:
            question_form = AddQuestion()
            return render(request, "blog/question_form2.html", {'form': question_form, 'mydict': mydict, 'isRoot': isRoot, 'parent':parent})


def upload_files(request):
    if request.method == 'POST':
        file_form = FileUploadForm(request.POST, request.FILES)
        if file_form.is_valid():
            file_form.save()
            mydict = handle_uploaded_file(request.FILES['file'])
            request.session['mydict'] = mydict
            request.session['parent'] = file_form['parent'].value()
            request.session['isRoot'] = file_form['isRoot'].value()
            return redirect(add_question)
        else:
            return render(request, "blog/upload_questions.html", {'form': file_form})
    else:
        file_form = FileUploadForm()
        return render(request, "blog/upload_questions.html", {'form': file_form})


class QuestionListView(ListView):
    model = QuestionBank
    template_name = 'blog/home.html' #<app>/<model>_<ListView>.html
    context_object_name = 'questionBanks'
    ordering = ['date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Home"
        return context


class QuizListView(ListView):
    model = QuizPaper
    template_name = 'blog/quizpapers_list.html' #<app>/<model>_<ListView>.html
    context_object_name = 'quizPapers'
    ordering = ['date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Quiz Papers"
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


class QuizCreateView(LoginRequiredMixin,CreateView):
    model = QuizPaper
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create new quiz"
        return context


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
        form.save()
        if form.cleaned_data['isRoot'] == 0:
            set_marks(form.cleaned_data['parent'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create new post"
        return context


def set_marks(id):
    qm = QuestionModule.objects.get(pk=id)
    qs = Question.objects.filter(parent=id,isRoot=0)
    qms = QuestionModule.objects.filter(parent=id, isRoot=0)
    marks = 0
    for q in qs:
        marks += q.marks
    for q in qms:
        marks += q.marks
    qm.marks = marks
    qm.save()
    if qm.isRoot == 0:
        set_marks(qm.parent)



class QuizDetailView(DetailView):
    model = QuizPaper
    template_name = 'blog/quizpaper_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Bank Details"
        self.object = self.get_object()
        qids =self.object.qid_list.split(",")[1:]
        qmids = self.object.qmid_list.split(",")[1:]
        context['qs'] = Question.objects.filter(pk__in=qids)
        context['qms'] = QuestionModule.objects.filter(pk__in=qmids)
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


class QuestionModuleDetailViewQuiz(DetailView):
    model = QuestionModule
    template_name = 'blog/quizquestionmodule_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Module Details"
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


class QuestionDetailViewQuiz(DetailView):
    model = Question
    template_name = 'blog/quizquestion_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Details"
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'blog/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Question Details"
        return context


class QuizUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = QuizPaper
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Quiz Paper"
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
    fields = ['statement', 'parent', 'isRoot']

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
    fields = ['statement', 'answer', 'marks', 'difficulty', 'tags', 'parent', 'isRoot']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        if form.cleaned_data['isRoot'] == 0:
            set_marks(form.cleaned_data['parent'])
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
        delete_module(self.object.id)
        self.object.delete()
        if self.object.isRoot == 0:
            set_marks(self.object.parent)
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
        id = self.object.id
        delete_bank(id)
        self.object.delete()
        return redirect(success_url)


class QuizDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = QuizPaper
    success_url = "/quizzes/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Delete Quiz"
        return context


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

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if self.object.isRoot == 0:
            set_marks(self.object.parent)
        return redirect(success_url)


def delete_bank(id):
    qs = Question.objects.filter(parent=id, isRoot=1)
    for q in qs:
        q.delete()
    qms = QuestionModule.objects.filter(parent=id, isRoot=1)
    for qm in qms:
        delete_module(qm.id)
        qm.delete()


def delete_module(id):
    qus = Question.objects.filter(parent=id, isRoot=0)
    print("start")
    for q in qus:
        q.delete()
    qms = QuestionModule.objects.filter(parent=id, isRoot=0)
    for qm in qms:
        delete_module(qm.id)
        qm.delete()
    print("end")