from django.shortcuts import render
from .forms import MyUserCreationForm
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
    redirect_authenticated_user = True
    template_name = './authentication/login.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('register')
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.layout = Layout(
            Div(
                HTML('''<h1 class="h3 mb-3 font-weight-normal">Джуманджи</h1>
            <p class="h5 font-weight-light">Создайте аккаунт</p>'''), css_class='text-center mt-5 b-1'
            ),
            AppendedText('username', ''),
            AppendedText('password', ''),
        )

