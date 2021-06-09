import os

import django
from django.db.models import Sum, Min, Count

import data

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from vacancies.models import Company, Specialty, Vacancy

print(Vacancy.objects.values('salary_min').annotate(Count('')))