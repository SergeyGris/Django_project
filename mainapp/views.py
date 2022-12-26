import logging

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    UserPassesTestMixin, LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseNotFound, \
    JsonResponse, FileResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, \
    DetailView, DeleteView, CreateView
from django.shortcuts import get_object_or_404

from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Course, CourseTeacher, Lesson, CourseFeedback

logger = logging.getLogger(__name__)


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


class CoursesListView(ListView):
    template_name = "mainapp/courses_list.html"
    model = Course

    # def get_context_data(self, **kwargs):
    #     context = super(CoursesListView, self).get_context_data(**kwargs)
    #     context["objects"] = Course.objects.all()[:7]
    #     return context


class CourseDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(Course, pk=pk)
        context["lessons"] = Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = CourseTeacher.objects.filter(course=context["course_object"])
        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(
                    course=context["course_object"], user=self.request.user
            ).count():
                context["feedback_form"] = CourseFeedbackForm(
                    course=context["course_object"], user=self.request.user
                )

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = (
                CourseFeedback.objects.filter(course=context["course_object"])
                    .order_by("-created", "-rating")[:5]
                    .select_related()
            )
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)  # 5 minutes
        else:
            context["feedback_list"] = cached_feedback

        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsListView(ListView):
    model = News
    template_name = "mainapp/news_list.html"
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class NewsDetailView(DetailView):
    model = News


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'  # для отображения всех полей в модели
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'  # для отображения всех полей в модели
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    fields = '__all__'  # для отображения всех полей в модели
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:  # first 1000 lines
                    break
                log_slice.insert(0, line)  # append at start
            context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
