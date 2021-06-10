from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, ListView

from vacancies.models import Company, Vacancy, Resume


class CompanyOrResumeLetsStartView(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.model.objects.get(owner=request.user)
        except self.model.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.redirect_url)


class MyCompanyLetsStartView(CompanyOrResumeLetsStartView):
    template_name = 'vacancies/user_profile/company-create.html'
    model = Company
    redirect_url = 'my_company'


class MyResumeLetsStartView(CompanyOrResumeLetsStartView):
    template_name = 'vacancies/user_profile/resume-create.html'
    model = Resume
    redirect_url = 'my_resume'


class CompanyOrResumeUpdateView(LoginRequiredMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.model.objects.get(owner=self.request.user)
        except self.model.DoesNotExist:
            return redirect(self.redirect_url)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.object


class MyCompanyUpdateView(CompanyOrResumeUpdateView):
    model = Company
    template_name = 'vacancies/user_profile/company-edit.html'
    fields = ['name', 'location', 'logo', 'description', 'employee_count']

    success_url = reverse_lazy('my_company')
    redirect_url = 'my_company_lets_start'


class MyResumeUpdateView(CompanyOrResumeUpdateView):
    model = Resume
    template_name = 'vacancies/user_profile/resume-edit.html'
    fields = ['name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio']

    success_url = reverse_lazy('my_resume')
    redirect_url = 'my_resume_lets_start'


class CompanyOrResumeCreateView(LoginRequiredMixin, CreateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.model.objects.get(owner=request.user)
        except self.model.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.redirect_url)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyCreateView(CompanyOrResumeCreateView):
    model = Company
    template_name = 'vacancies/user_profile/company-edit.html'
    fields = ['name', 'location', 'logo', 'description', 'employee_count']

    success_url = reverse_lazy('my_company')
    redirect_url = 'my_company'


class MyResumeCreateView(CompanyOrResumeCreateView):
    model = Resume
    template_name = 'vacancies/user_profile/resume-edit.html'
    fields = ['name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio']

    success_url = reverse_lazy('my_resume')
    redirect_url = 'my_resume'


class MyVacanciesView(LoginRequiredMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/user_profile/vacancy-list.html'

    def get_queryset(self):
        return (
            self.model.objects
            .filter(company__owner=self.request.user)
            .select_related('company')
        )


class MyVacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'vacancies/user_profile/vacancy-edit.html'
    fields = ['title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.company = Company.objects.get(owner=self.request.user)
        except self.model.DoesNotExist:
            return redirect('my_company_lets_start')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.object = self.company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_vacancies')


class MyVacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacancy
    template_name = 'vacancies/user_profile/vacancy-edit.html'
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
        form.instance.object = self.company
        return super().form_valid(form)

