from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from authentication.views import MyRegisterView, MyLoginView
from vacancies.views import ListVacanciesByCompanyView, DetailVacancyView, MyCompanyUpdateView, MyCompanyCreateView, \
    MyCompanyLetsStartView, ApplicationSendView
from vacancies.views import ListVacanciesView, ListVacanciesBySpecialtyView
from vacancies.views import MainView
from vacancies.views import custom_handler404, custom_handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='home'),
    path('vacancy/', ListVacanciesView.as_view(), name='all_vacancies'),
    path('vacancy/cat/<specialty>', ListVacanciesBySpecialtyView.as_view(), name='vacancies_by_speciality'),
    path('vacancy/<int:pk>', DetailVacancyView.as_view(), name='vacancy'),
    path('companies/<int:pk>', ListVacanciesByCompanyView.as_view(), name='company'),

    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('vacancies/<int:pk>/send/', ApplicationSendView, name='application_send'),

    path('mycompany/letsstart/', MyCompanyLetsStartView.as_view(), name='my_company_lets_start'),
    path('mycompany/', MyCompanyUpdateView.as_view(), name='my_company'),
    path('mycompany/create', MyCompanyCreateView.as_view(), name='my_company_create'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500
