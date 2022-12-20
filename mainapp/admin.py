from django.contrib import admin
from django.utils.html import format_html

from mainapp.models import News, Course, Lesson, CourseTeacher

# Register your models here.

# admin.site.register(News)
admin.site.register(Course)
admin.site.register(CourseTeacher)
admin.site.register(Lesson)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_deleted', 'slug')
    list_filter = ('is_deleted',)
    ordering = ('pk',)
    list_per_page = 5
    search_fields = ('title', 'preamble', 'body',)
    actions = ('mark_as_deleted',)

    def slug(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )

    slug.short_description = 'Слаг'

    def mark_as_deleted(self, request, queryset):
        queryset.update(is_deleted=True)

    mark_as_deleted.short_description = 'Пометить удаленным'
