from django.contrib import admin
from django.urls import path

from vacancies.views import DetailCompanyView, DetailVacancyView
from vacancies.views import ListVacanciesView, ListVacanciesBySpecialtyView
from vacancies.views import MainView
from vacancies.views import custom_handler404, custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='home'),
    path('vacancies/', ListVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<specialty>', ListVacanciesBySpecialtyView.as_view(), name='vacancies_by_speciality'),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name='vacancy'),
    path('companies/<int:pk>', DetailCompanyView.as_view(), name='company'),
]

handler404 = custom_handler404
handler500 = custom_handler500
