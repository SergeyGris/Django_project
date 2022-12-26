from django.views.decorators.cache import cache_page

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name="contacts"),
    path('courses_list/', cache_page(60 * 5)(views.CoursesListView.as_view()), name="courses"),
    path('', views.IndexView.as_view(), name="index"),
    path('docsite/', views.DocSiteView.as_view(), name="doc_site"),
    path("courses/<int:pk>/detail/", views.CourseDetailView.as_view(), name="courses_detail"),
    path("courses/feedback/", views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),

    # News
    path('news/', views.NewsListView.as_view(), name="news"),
    path('news/add/', views.NewsCreateView.as_view(), name="news_create"),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name="news_update"),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name="news_detail"),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name="news_delete"),

    # logs
    path("log_view/", views.LogView.as_view(), name="log_view"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
