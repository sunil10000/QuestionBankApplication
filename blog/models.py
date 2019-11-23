from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import TextInput, Textarea
from django.core.validators import FileExtensionValidator
from QuestionBankApplication import  settings


class Question(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #If the user is deleted, its post will also be deleted

    statement = models.TextField()
    answer = models.TextField(blank=True, null=True)
    marks = models.PositiveIntegerField()
    tags = models.TextField()

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


class QuestionBank(models.Model):
    title = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('bank-detail', kwargs={'pk': self.pk})


class UploadedFile(models.Model):
    file = models.FileField(upload_to="QuestionFiles",
                            validators=[FileExtensionValidator(allowed_extensions=['ini'])])
