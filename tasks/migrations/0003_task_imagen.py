# Generated by Django 5.1.1 on 2024-09-25 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_datecompleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='tasks_images/'),
        ),
    ]
