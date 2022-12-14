from django.urls import path
from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name="contacts"),
    path('courses_list/', views.CoursesListView.as_view(), name="courses"),
    path('', views.IndexView.as_view(), name="index"),
    path('docsite/', views.DocSiteView.as_view(), name="doc_site"),
    path("courses/<int:pk>/detail/", views.CourseDetailView.as_view(), name="courses_detail", ),
    path("courses/feedback/", views.CourseFeedbackCreateView.as_view(), name="course_feedback", ),

    # News
    path('news/', views.NewsListView.as_view(), name="news"),
    path('news/add/', views.NewsCreateView.as_view(), name="news_create"),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name="news_update"),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name="news_detail"),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name="news_delete"),

]
