from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field
from django import forms

from .models import Application, Company, Vacancy, Resume


class CustomImageInput(Field):
    template = 'crispy_forms/custom_image_input.html'


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.fields['written_username'].label = 'Вас зовут'
        self.fields['written_phone'].label = 'Ваш телефон'
        self.fields['written_cover_letter'].label = 'Сопроводительное письмо'

        self.helper.layout = Layout(
            Div(
                Div(
                    'written_username',
                    'written_phone',
                    'written_cover_letter',
                    Submit('submit', 'Отправить отклик'),
                    css_class='card-body mx-3',
                ),
                css_class='card mt-4 mb-3',
            ),
        )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.fields['name'].label = 'Название компании'
        self.fields['location'].label = 'География'
        self.fields['logo'].label = 'Логотип'
        self.fields['description'].label = 'Информация о компании'
        self.fields['employee_count'].label = 'Количество человек в компании'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-12 col-md-6'),
                CustomImageInput('logo'),
            ),
            Row(
                Column('employee_count', css_class='col-12 col-md-6'),
                Column('location', css_class='col-12 col-md-6'),
            ),
            'description',

            Submit('submit', 'Сохранить'),
        )


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.fields['title'].label = 'Название вакансии'
        self.fields['specialty'].label = 'Специализация'
        self.fields['skills'].label = 'Требуемые навыки'
        self.fields['skills'].widget.attrs = {'rows': 3}
        self.fields['description'].label = 'Описание вакансии'
        self.fields['description'].widget.attrs = {'rows': 13}
        self.fields['salary_min'].label = 'Зарплата от'
        self.fields['salary_max'].label = 'Зарплата до'

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-12 col-md-6'),
                Column('specialty', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('salary_min', css_class='col-12 col-md-6'),
                Column('salary_max', css_class='col-12 col-md-6'),
            ),
            'skills',
            'description',

            Submit('submit', 'Сохранить'),
        )


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio']

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.fields['name'].label = 'Имя'
        self.fields['surname'].label = 'Фамилия'
        self.fields['status'].label = 'Готовность к работе'
        self.fields['salary'].label = 'Ожидаемое вознаграждение'
        self.fields['specialty'].label = 'Специализация'
        self.fields['grade'].label = 'Квалификация'
        self.fields['education'].label = 'Образование'
        self.fields['education'].widget.attrs = {'rows': 4}
        self.fields['experience'].label = 'Опыт работы'
        self.fields['experience'].widget.attrs = {'rows': 4}
        self.fields['portfolio'].label = 'Ссылка на портфолио'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-12 col-md-6'),
                Column('surname', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('status', css_class='col-12 col-md-6'),
                Column('salary', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('specialty', css_class='col-12 col-md-6'),
                Column('grade', css_class='col-12 col-md-6'),
            ),
            'education',
            'experience',
            'portfolio',

            Submit('submit', 'Сохранить'),
        )
