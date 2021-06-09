from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, ListView

from vacancies.models import Company, Vacancy


class MyCompanyLetsStartView(LoginRequiredMixin, TemplateView):
    template_name = 'vacancies/my_company/company-create.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('my_company')


class MyCompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'vacancies/my_company/company-edit.html'
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
    template_name = 'vacancies/my_company/company-edit.html'
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

class MyVacanciesView(LoginRequiredMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/my_company/vacancy-list.html'

    def get_queryset(self):
        return (
            self.model.objects
            .filter(company__owner=self.request.user)
            .select_related('company')
        )


class MyVacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'vacancies/my_company/vacancy-edit.html'
    fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.company = Company.objects.get(owner=self.request.user)
        except self.model.DoesNotExist:
            return redirect('my_company_lets_start')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_vacancies')


class MyVacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacancy
    template_name = 'vacancies/my_company/vacancy-edit.html'
    fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']
    success_url = reverse_lazy('my_vacancies')
    context_object_name = 'vacancy'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.company = Company.objects.get(owner=self.request.user)
        except self.model.DoesNotExist:
            return redirect('my_company_lets_start')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(company=self.company)

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)

