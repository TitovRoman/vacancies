import os

import django

import data

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from vacancies.models import Company, Specialty, Vacancy


def import_specialities_to_db():
    specialty_images = {
        'frontend': 'specty_frontend.png',
        'backend': 'specty_backend.png',
        'gamedev': 'specty_gamedev.png',
        'devops': 'specty_devops.png',
        'design': 'specty_design.png',
        'products': 'specty_products.png',
        'management': 'specty_management.png',
        'testing': 'specty_testing.png',
    }
    for specialty in data.specialties:
        specialty_obj = Specialty(
            code=specialty['code'],
            title=specialty['title'],
        )
        try:
            specialty_obj.picture = specialty_images[specialty['code']]
        except KeyError:
            pass
        specialty_obj.save()


def import_companies_and_jobs_to_db():
    companies = {}
    for company in data.companies:
        companies[company['id']] = Company.objects.create(
            name=company['title'],
            location=company['location'],
            logo=company['logo'],
            description=company['description'],
            employee_count=company['employee_count'],
        )

    for job in data.jobs:
        Vacancy.objects.create(
            title=job['title'],
            specialty=Specialty.objects.get(code=job['specialty']),
            company=companies[job['company']],
            skills=job['skills'].replace(',', ' •'),
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )


if __name__ == '__main__':
    import_specialities_to_db()
    import_companies_and_jobs_to_db()
