from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView
from django.shortcuts import render

from vacancies.models import Company, Specialty, Vacancy


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count=Count('vacancy')).order_by('id')
        context['companies'] = Company.objects.annotate(count=Count('vacancy')).order_by('id')

        return context


class ListVacanciesByCompanyView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/company/company.html'

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
    template_name = 'vacancies/vacancy/vacancy.html'
    queryset = model.objects.select_related('specialty', 'company')


class ListVacanciesView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancy/vacancies.html'
    queryset = model.objects.select_related('specialty', 'company')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_title'] = 'Все вакансии'

        return context


class ListVacanciesBySpecialtyView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancy/vacancies.html'

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


class ApplicationSendView(TemplateView):
    template_name = 'vacancies/resume/send.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy_pk'] = self.kwargs['pk']

        return context


class MyCompanyLetsStartView(LoginRequiredMixin, TemplateView):
    template_name = 'vacancies/company/company-create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            print("Here")
            Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('my_company')


class MyCompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'vacancies/company/company-edit.html'
    fields = ['name', 'location', 'logo', 'description', 'employee_count']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.company = self.model.objects.get(owner=self.request.user)
        except self.model.DoesNotExist:
            return redirect('my_company_lets_start')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.company

    def get_success_url(self):
        return reverse('my_company')


class MyCompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'vacancies/company/company-edit.html'
    fields = ['name', 'location', 'logo', 'description', 'employee_count']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.model.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('my_company')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_company')


def custom_handler404(request, exception):
    return HttpResponseNotFound("404 Страница не найдена")


def custom_handler500(request):
    return HttpResponseServerError("500 Server Error")
