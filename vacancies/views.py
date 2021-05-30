from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from vacancies.models import Company, Specialty, Vacancy


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count=Count('vacancies')).order_by('id')
        context['companies'] = Company.objects.annotate(count=Count('vacancies')).order_by('id')

        return context


class ListVacanciesByCompanyView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/company.html'

    def get_queryset(self):
        return (
            self.model.objects
            .filter(company__id=self.kwargs['pk'])
            .select_related('specialty', 'company')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(Company, id=self.kwargs['pk'])

        return context


class DetailVacancyView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'vacancies/vacancy.html'
    queryset = model.objects.select_related('specialty', 'company')


class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancies.html'
    queryset = model.objects.select_related('specialty', 'company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = 'Все вакансии'

        return context


class ListVacanciesBySpecialtyView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancies.html'

    def get_queryset(self):
        return (
            self.model.objects
            .filter(specialty__code=self.kwargs['specialty'])
            .select_related('specialty', 'company')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = self.kwargs['specialty']

        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound("404 Страница не найдена")


def custom_handler500(request):
    return HttpResponseServerError("500 Server Error")
