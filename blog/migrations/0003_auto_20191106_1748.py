# Generated by Django 2.2.7 on 2019-11-06 17:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20191106_1730'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='QuestionBank',
        ),
    ]