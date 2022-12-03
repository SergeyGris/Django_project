
from django.http import  HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from mainapp.models import News, Courses, CourseTeachers, Lesson


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'address': 'территория Петропавловская крепость, 3Ж'
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'address': 'территория Кремль, 11, Казань, Республика Татарстан, Россия'
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-333333',
                'email': 'geeklab@msk.ru',
                'address': 'Красная площадь, 7, Москва, Россия'
            }

        ]
        return context_data


class CoursesView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class CoursesListView(TemplateView):
    template_name = "mainapp/courses_list.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context["objects"] = Courses.objects.all()[:7]
        return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Courses, pk=pk)
        context["lessons"] = Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = CourseTeachers.objects.filter(course=context["course_object"])
        return context

class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # with open(settings.BASE_DIR / 'news.json',
        #           encoding='utf-8') as news_file:
        context_data['object_list'] = News.objects.all()
        return context_data


def get(self, *args, **kwargs):
    query = self.request.GET.get('q', None)
    if query:
        return HttpResponseRedirect(f'https://google.com/search?q={query}')
    return super().get(*args, **kwargs)


class NewsWithPaginatorView(NewsView):
    def get_context_data(self, page, **kwargs):
        context_data = super().get_context_data(page=page, **kwargs)
        context_data["page_num"] = page
        return context_data
