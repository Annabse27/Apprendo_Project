# Generated by Django 5.1.2 on 2024-11-06 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_answer_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Правильный ответ'),
        ),
    ]
