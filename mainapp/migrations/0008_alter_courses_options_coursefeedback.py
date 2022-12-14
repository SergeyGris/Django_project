# Generated by Django 4.1.3 on 2022-12-20 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0007_courses_is_deleted_lesson_is_deleted_news_is_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courses',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.CreateModel(
            name='CourseFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Даата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('rating', models.PositiveSmallIntegerField(choices=[(5, '⭐⭐⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (2, '⭐⭐'), (1, '⭐')], default=5, verbose_name='Рейтинг')),
                ('feedback', models.TextField(default='Без отзыва', verbose_name='Отзыв')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.courses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
    ]
