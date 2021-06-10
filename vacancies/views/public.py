from django.db.models import Count, Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from vacancies.forms import ApplicationForm
from vacancies.models import Specialty, Company, Vacancy


class MainView(TemplateView):
    template_name = 'vacancies/index.html'
    search_examples = ['Python', 'Flask', 'Django', 'Парсинг', 'ML']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count=Count('vacancies')).order_by('id')
        context['companies'] = Company.objects.annotate(count=Count('vacancies')).order_by('id')
        context['search_examples'] = self.search_examples

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


class VacancyWithApplicationView(View):
    template_name = 'vacancies/vacancy/vacancy.html'

    def dispatch(self, request, *args, **kwargs):
        # try:
        #     self.vacancy = Vacancy.objects.select_related('specialty', 'company').get(id=self.kwargs['pk'])
        # except Vacancy.DoesNotExist:
        #     raise Http404('No %s matches the given query.' % Vacancy._meta.object_name)

        self.vacancy = get_object_or_404(Vacancy.objects.select_related('specialty', 'company'), id=self.kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'vacancy': self.vacancy,
            'application_form': ApplicationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        application_form = ApplicationForm(request.POST)
        application_form.instance.vacancy = self.vacancy
        application_form.instance.user = request.user if request.user.is_authenticated else None
        if application_form.is_valid():
            application_form.save()
            return redirect('application_send', self.vacancy.id)

        return render(request, self.template_name, context={
            'vacancy': self.vacancy,
            'application_form': application_form,
        })


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
    template_name = 'vacancies/vacancy/application_send.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy_pk'] = self.kwargs['pk']

        return context


class VacanciesSearchView(ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/vacancy/search.html'

    def dispatch(self, request, *args, **kwargs):
        self.search_line = self.request.GET.get('s', '')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            self.model.objects
            .filter(
                Q(title__icontains=self.search_line) |
                Q(skills__icontains=self.search_line) |
                Q(description__icontains=self.search_line) |
                Q(specialty__title__icontains=self.search_line)
            )
            .select_related('specialty', 'company')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_line'] = self.search_line


        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound("404 Страница не найдена")


def custom_handler500(request):
    return HttpResponseServerError("500 Server Error")