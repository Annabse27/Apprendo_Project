# Generated by Django 5.1.2 on 2024-11-01 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0007_question_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=255),
        ),
    ]