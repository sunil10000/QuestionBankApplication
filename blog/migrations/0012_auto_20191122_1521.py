# Generated by Django 2.2.7 on 2019-11-22 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20191122_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='parent',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
