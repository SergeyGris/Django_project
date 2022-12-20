from django.urls import path

from authapp import views
from authapp.views import RegisterView,ProfileEditView, CustomLoginView, CustomLogoutView
from authapp.apps import AuthappConfig

app_name = AuthappConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("edit/", ProfileEditView.as_view(), name="edit"),

    ]
