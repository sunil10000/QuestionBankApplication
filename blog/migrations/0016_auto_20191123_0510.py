# Generated by Django 2.2.7 on 2019-11-23 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_questionbank_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionbank',
            name='title',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
