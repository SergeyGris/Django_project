from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _

from authapp import forms
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


# Create your views here.
class ProfileEditView( UpdateView):
    model = User
    form_class = forms.CustomUserChangeForm
    template_name = 'authapp/edit.html'


    def get_object(self, queryset=None):
        return self.request.user
        # return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:edit", args=[self.request.user.pk])


class CustomLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:index')


# class RegisterView(TemplateView):
#     template_name = 'authapp/register.html'
#     extra_context = {
#         'title': 'Регистрация'
#     }
#
#     def post(self, request, *args, **kwargs):
#         try:
#             if all(
#                     (
#                             request.POST.get('username'),
#                             request.POST.get('email'),
#                             request.POST.get('password1'),
#                             request.POST.get('password2'),
#                             request.POST.get('first_name'),
#                             request.POST.get('last_name'),
#                             request.POST.get('password1') == request.POST.get('password2'),
#                     )
#
#             ):
#                 new_user = User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     email=request.POST.get('email'),
#                     age=request.POST.get('age') if request.POST.get('age') else 0,
#                     avatar=request.FILES.get('avatar'),
#                 )
#                 print(new_user)
#                 new_user.set_password(request.POST.get('password1'))
#                 new_user.save()
#                 messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#             else:
#                 messages.add_message(request, messages.WARNING, 'Что-то пошло не так')
#                 return HttpResponseRedirect(reverse('authapp:register'))
#         except Exception as ex:
#             messages.add_message(request, messages.WARNING, 'Что-то пошло не так')
#             return HttpResponseRedirect(reverse('authapp:register'))
#

# class CustomLoginView(LoginView):
#     template_name = 'authapp/login.html'
#     extra_context = {
#         'title': 'Вход'
#     }

class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'

    def form_valid(self, form):
        ret = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))
