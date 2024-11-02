# Generated by Django 5.1.2 on 2024-11-01 00:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_question_answer_test_question_test'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='owner',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='owned_questions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
