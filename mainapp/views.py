from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, DeleteView, CreateView
from django.shortcuts import get_object_or_404

from mainapp.forms import CourseFeedbackForm
from mainapp.models import News, Course, CourseTeacher, Lesson, CourseFeedback


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
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super(CourseDetailView, self).get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CourseTeacher.objects.filter(course=context_data['course_object'])
        context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])

        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(
                course=context_data['course_object'],
                user=self.request.user
            )
        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item'})
        return JsonResponse({'card': rendered_template})


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
