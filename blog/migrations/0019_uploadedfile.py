# Generated by Django 2.2.7 on 2019-11-23 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20191123_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='QuestionFiles', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ini'])])),
            ],
        ),
    ]
