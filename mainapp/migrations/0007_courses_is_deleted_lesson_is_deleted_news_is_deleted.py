# Generated by Django 4.1.3 on 2022-12-03 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_courseteachers_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
        migrations.AddField(
            model_name='news',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
    ]
