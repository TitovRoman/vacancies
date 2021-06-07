from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Fieldset
from crispy_forms.bootstrap import PrependedText, AppendedText, FormActions

class MyUserCreationForm(UserCreationForm):
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
            AppendedText('password1', ''),
            AppendedText('password2', ''),
        )