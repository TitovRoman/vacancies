from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from vacancies.models import Company, Specialty, Vacancy


def main_view(request):
    context = {
        'specialties': Specialty.objects.annotate(count=Count('vacancies')).order_by('id'),
        'companies': Company.objects.annotate(count=Count('vacancies')).order_by('id'),
    }
    return render(request, 'vacancies/index.html', context=context)


class DetailCompanyView(DetailView):
    model = Company
    context_object_name = 'company'
    template_name = 'vacancies/company.html'

    # def get_queryset(self):
    #     return Company.objects.filter(id=self.kwargs['pk'])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['vacancies'] = Vacancy.objects.()


class DetailVacancyView(DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'vacancies/vacancy.html'


class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = 'Все вакансии'

        return context


class ListVacanciesBySpecialtyView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancies.html'

    def get_queryset(self):
        return self.model.objects.filter(specialty__code=self.kwargs['specialty'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = self.kwargs['specialty']

        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound("404 Страница не найдена")


def custom_handler500(request):
    return HttpResponseServerError("500 Server Error")
