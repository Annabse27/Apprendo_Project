# Generated by Django 5.1.2 on 2024-11-02 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0011_test_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
