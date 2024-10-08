# Generated by Django 5.0.7 on 2024-08-22 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0005_alter_task_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last update time')),
                ('tasks', models.ManyToManyField(related_name='labels', to='tasks.task')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]
