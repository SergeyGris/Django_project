# Generated by Django 4.1.3 on 2022-12-03 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_data_load'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Даата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_as_markdown', models.BooleanField(default=False, verbose_name='As markdown')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Cost')),
                ('cover', models.CharField(default='no_image.svg', max_length=25, verbose_name='Cover')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='news',
            old_name='if_deleted',
            new_name='is_deleted',
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Даата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('num', models.PositiveIntegerField(verbose_name='Lesson number')),
                ('title', models.CharField(max_length=256, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_as_markdown', models.BooleanField(default=False, verbose_name='As markdown')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.courses')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
                'ordering': ('course', 'num'),
            },
        ),
        migrations.CreateModel(
            name='CourseTeachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Даата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('name_first', models.CharField(max_length=128, verbose_name='Name')),
                ('name_second', models.CharField(max_length=128, verbose_name='Surname')),
                ('day_birth', models.DateField(verbose_name='Birth date')),
                ('course', models.ManyToManyField(to='mainapp.courses')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
