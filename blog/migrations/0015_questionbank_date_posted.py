# Generated by Django 2.2.7 on 2019-11-23 05:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20191122_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionbank',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]