from django.contrib.auth import get_user_model
from django.db import models

NULLABLE = {"blank": True, "null": True}


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Даата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата последнего изменения')

    is_deleted = models.BooleanField(default=False, verbose_name='Удален')

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class NewsManager(models.Manager):
    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class News(BaseModel):
    objects = NewsManager
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1000, verbose_name='Вступление')
    body = models.TextField(verbose_name='Содержание')
    body_as_markdown = models.BooleanField(default=False,
                                           verbose_name='Способ разметки')

    def __str__(self):
        return f'#{self.pk} {self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ('-created_at',)


class CourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Course(BaseModel):
    objects = CourseManager()

    name = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", blank=True,
                                   null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown",
                                                  default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2,
                               verbose_name="Cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg",
                             verbose_name="Cover")

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown",
                                                  default=False)

    def __str__(self) -> str:
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        ordering = ("course", "num")
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseTeacher(models.Model):
    course = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second,
                                        self.name_first)


class CourseFeedback(BaseModel):
    RATING_FIVE = 5
    RATINGS = (
        (RATING_FIVE, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(choices=RATINGS, default=RATING_FIVE, verbose_name='Рейтинг')
    feedback = models.TextField(verbose_name='Отзыв', default='Без отзыва')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'Отзыв на {self.course} от {self.user}'
