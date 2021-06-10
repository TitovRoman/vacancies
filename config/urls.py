from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from authentication.views import MyRegisterView, MyLoginView
from vacancies.views.public import DetailVacancyView, ApplicationSendView, VacancyWithApplicationView, \
    VacanciesSearchView
from vacancies.views.user_profile import MyCompanyLetsStartView, MyCompanyUpdateView, MyCompanyCreateView, \
    MyVacanciesView, MyVacancyCreateView, MyVacancyUpdateView, MyResumeLetsStartView, MyResumeUpdateView, \
    MyResumeCreateView
from vacancies.views.public import ListVacanciesView, ListVacanciesBySpecialtyView, ListVacanciesByCompanyView
from vacancies.views.public import MainView
from vacancies.views.public import custom_handler404, custom_handler500



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='home'),
    path('vacancies/', ListVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<specialty>', ListVacanciesBySpecialtyView.as_view(), name='vacancies_by_speciality'),
    path('vacancies/<int:pk>', VacancyWithApplicationView.as_view(), name='vacancy'),
    path('companies/<int:pk>', ListVacanciesByCompanyView.as_view(), name='company'),

    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('vacancies/<int:pk>/send/', ApplicationSendView.as_view(), name='application_send'),

    path('mycompany/letsstart/', MyCompanyLetsStartView.as_view(), name='my_company_lets_start'),
    path('mycompany/', MyCompanyUpdateView.as_view(), name='my_company'),
    path('mycompany/create', MyCompanyCreateView.as_view(), name='my_company_create'),

    path('mycompany/vacancies/', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/create', MyVacancyCreateView.as_view(), name='my_vacancy_create'),
    path('mycompany/vacancies/<int:pk>', MyVacancyUpdateView.as_view(), name='my_vacancy_update'),

    path('myresume/letsstart/', MyResumeLetsStartView.as_view(), name='my_resume_lets_start'),
    path('myresume/', MyResumeUpdateView.as_view(), name='my_resume'),
    path('myresume/create', MyResumeCreateView.as_view(), name='my_resume_create'),

    path('search/', VacanciesSearchView.as_view(), name='vacancies_search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500
