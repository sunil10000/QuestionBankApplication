# Generated by Django 2.2.7 on 2019-11-06 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_questionbank_date_posted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionbank',
            name='file_field',
        ),
    ]
