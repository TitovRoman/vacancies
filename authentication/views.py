from django.shortcuts import render
from .forms import MyUserCreationForm, MyAuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Fieldset
from crispy_forms.bootstrap import PrependedText, AppendedText, FormActions

from django.conf import settings

class MyRegisterView(CreateView):
   form_class = MyUserCreationForm
   success_url = settings.LOGIN_URL
   template_name = './authentication/register.html'


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm
    redirect_authenticated_user = True
    template_name = './authentication/login.html'


