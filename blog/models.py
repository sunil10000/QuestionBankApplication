from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class QuestionBank(models.Model):
    title = models.CharField(max_length=300)
    file_field = models.FileField()
    date_posted=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #If the user is deleted, its post will also be deleted

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

#auto_now_add=True