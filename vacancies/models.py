from enum import Enum

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _







class SpecialtyChoices(Enum):
    frontend = 'Фронтенд'
    backend = 'Бэкенд'
    gamedev = 'Геймдев'
    devops = 'Девопс'
    design = 'Дизайн'
    products = 'Продукты'
    management = 'Менеджмент'
    testing = 'Тестирование'





class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f"Company {self.name}"


class Specialty(models.Model):
    code = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return f"{self.title}"


class Vacancy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if self.salary_min > self.salary_max:
            raise ValidationError({
                'salary_min': _('salary_min must be less or equal to salary_max'),
                'salary_max': _('salary_max must be greater or equal to salary_min'),
            })


class Application(models.Model):
    written_username = models.CharField(max_length=64)
    written_phone = models.CharField(max_length=32)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='applications')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f"Application with pk={self.pk}"


class Resume(models.Model):

    class WorkStatusChoices(models.TextChoices):
        not_in_search = 'Не ищу работу', _('Не ищу работу')
        consideration = 'Рассматриваю предложения', _('Рассматриваю предложения')
        in_search = 'Ищу работу', _('Ищу работу')

    class GradeChoices(models.TextChoices):
        intern = 'intern', _('Intern')
        junior = 'junior', _('Junior')
        middle = 'middle', _('Middle')
        senior = 'senior', _('Senior')
        lead = 'lead', _('Lead')

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    status = models.CharField(
        max_length=32,
        choices=WorkStatusChoices.choices,
        default=WorkStatusChoices.in_search,
    )
    salary = models.IntegerField()
    specialty = models.OneToOneField(Specialty, on_delete=models.CASCADE)
    grade = models.CharField(
        max_length=32,
        choices=GradeChoices.choices,
        default=GradeChoices.junior,
    )
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.URLField()

