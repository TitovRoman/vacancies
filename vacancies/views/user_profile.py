from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, ListView

from vacancies.forms import CompanyForm, VacancyForm, ResumeForm
from vacancies.models import Company, Vacancy, Resume


class ObjectNotRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.model.objects.get(owner=request.user)
        except self.model.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.redirect_url)


class ObjectRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = self.model.objects.get(owner=self.request.user)
        except self.model.DoesNotExist:
            return redirect(self.redirect_url)
        else:
            return super().dispatch(request, *args, **kwargs)


class CompanyOrResumeLetsStartView(LoginRequiredMixin, ObjectNotRequiredMixin, TemplateView):
    pass


class MyCompanyLetsStartView(CompanyOrResumeLetsStartView):
    template_name = 'vacancies/user_profile/company-create.html'
    model = Company
    redirect_url = 'my_company'


class MyResumeLetsStartView(CompanyOrResumeLetsStartView):
    template_name = 'vacancies/user_profile/resume-create.html'
    model = Resume
    redirect_url = 'my_resume'


class CompanyOrResumeUpdateView(LoginRequiredMixin, ObjectRequiredMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        http_referer = self.request.META.get('HTTP_REFERER')
        if (http_referer == self.request.build_absolute_uri(reverse(self.updated_url_name)) or
                http_referer == self.request.build_absolute_uri(reverse(self.create_url_name))):
            context['is_updated'] = True
        else:
            context['is_updated'] = False
        return context

    def get_object(self):
        return self.object


class MyCompanyUpdateView(CompanyOrResumeUpdateView):
    model = Company
    template_name = 'vacancies/user_profile/company-edit.html'
    form_class = CompanyForm

    success_url = reverse_lazy('my_company')
    redirect_url = 'my_company_lets_start'
    updated_url_name = 'my_company'
    create_url_name = 'my_company_create'


class MyResumeUpdateView(CompanyOrResumeUpdateView):
    model = Resume
    template_name = 'vacancies/user_profile/resume-edit.html'
    form_class = ResumeForm

    success_url = reverse_lazy('my_resume')
    redirect_url = 'my_resume_lets_start'
    updated_url_name = 'my_resume'
    create_url_name = 'my_resume_create'


class CompanyOrResumeCreateView(LoginRequiredMixin, ObjectNotRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MyCompanyCreateView(CompanyOrResumeCreateView):
    model = Company
    template_name = 'vacancies/user_profile/company-edit.html'
    form_class = CompanyForm

    success_url = reverse_lazy('my_company')
    redirect_url = 'my_company'


class MyResumeCreateView(CompanyOrResumeCreateView):
    model = Resume
    template_name = 'vacancies/user_profile/resume-edit.html'
    form_class = ResumeForm

    success_url = reverse_lazy('my_resume')
    redirect_url = 'my_resume'


class CompanyRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.company = Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            return redirect(self.redirect_url)
        else:
            return super().dispatch(request, *args, **kwargs)


class MyVacanciesView(LoginRequiredMixin, CompanyRequiredMixin, ListView):
    model = Vacancy
    context_object_name = 'vacancies'
    template_name = 'vacancies/user_profile/vacancy-list.html'
    redirect_url = 'my_company_lets_start'

    def get_queryset(self):
        return (
            self.model.objects
            .filter(company=self.company)
            .select_related('company')
            .prefetch_related('applications')
        )


class MyVacancyCreateView(LoginRequiredMixin, CompanyRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'vacancies/user_profile/vacancy-edit.html'
    form_class = VacancyForm
    redirect_url = 'my_company_lets_start'

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_vacancy_update', kwargs={'pk': self.object.id})


class MyVacancyUpdateView(LoginRequiredMixin, CompanyRequiredMixin, UpdateView):
    model = Vacancy
    template_name = 'vacancies/user_profile/vacancy-edit.html'

    form_class = VacancyForm
    context_object_name = 'vacancy'
    redirect_url = 'my_company_lets_start'
    updated_url_name = 'my_vacancy_update'
    create_url_name = 'my_vacancy_create'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(company=self.company).prefetch_related('applications')

    def form_valid(self, form):
        form.instance.object = self.company
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        http_referer = self.request.META.get('HTTP_REFERER')
        if (http_referer == self.request.build_absolute_uri(reverse(self.updated_url_name,
                                                                    kwargs={'pk': self.kwargs['pk']})) or
                http_referer == self.request.build_absolute_uri(reverse(self.create_url_name))):
            context['is_updated'] = True
        else:
            context['is_updated'] = False
        return context

    def get_success_url(self):
        return reverse('my_vacancy_update', kwargs={'pk': self.kwargs['pk']})
