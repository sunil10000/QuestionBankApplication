from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import TextInput, Textarea
from django.core.validators import FileExtensionValidator
from QuestionBankApplication import  settings
from django.core.validators import validate_comma_separated_integer_list


class Question(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #If the user is deleted, its post will also be deleted

    statement = models.TextField()
    answer = models.TextField(blank=True, null=True)
    marks = models.PositiveIntegerField()
    chapter_tag = models.CharField(max_length=1000)
    section_tag = models.CharField(max_length=1000)

    parent = models.PositiveIntegerField(null=True)
    isRoot = models.IntegerField()
    difficulty_Choices = (("Easy","Easy"),("Medium", "Medium"), ("Hard","Hard"))

    difficulty = models.CharField(max_length=9, choices=difficulty_Choices, default="Medium")

    formfield_overrides = {
        models.CharField : {'widget': TextInput(attrs={'size':20})},
        models.TextField : {'widget': Textarea(attrs={'rows':4, 'cols':40})}
    }

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    # class Meta:
    #     unique_together = ('statement', 'parent', 'isRoot')


class QuestionModule(models.Model):
    statement = models.TextField()
    marks = models.PositiveIntegerField()
    parent = models.PositiveIntegerField()
    isRoot = models.IntegerField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }

    def get_absolute_url(self):
        return reverse('module-detail', kwargs={'pk': self.pk})

    # class Meta:
    #     unique_together = ('statement', 'parent', 'isRoot')


class QuestionBank(models.Model):
    title = models.CharField(max_length=1000) #, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('bank-detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     self.validate_unique()
    #     super(QuestionBank, self).save(*args, **kwargs)


class UploadedFile(models.Model):
    file = models.FileField(upload_to="QuestionFiles",
                            validators=[FileExtensionValidator(allowed_extensions=['ini'])])
    title = models.CharField(max_length=1000)
    parent = models.PositiveIntegerField()
    isRoot = models.IntegerField()


class QuizPaper(models.Model):
    title = models.CharField(max_length=1000)  #, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    qid_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1000)
    qmid_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('quiz-detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     self.validate_unique()
    #     super(QuizPaper, self).save(*args, **kwargs)


class JustToChose(models.Model):
    choices = ()
    option = models.CharField(max_length=9, choices=choices)
