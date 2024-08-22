# Generated by Django 5.0.7 on 2024-08-22 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0005_alter_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='labels', to='tasks.task'),
        ),
    ]
