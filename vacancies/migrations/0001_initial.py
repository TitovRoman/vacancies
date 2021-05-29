# Generated by Django 3.2.2 on 2021-05-29 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('logo', models.URLField(default='https://place-hold.it/100x60')),
                ('description', models.TextField()),
                ('employee_count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(max_length=64)),
                ('picture', models.URLField(default='https://place-hold.it/100x60')),
            ],
            options={
                'verbose_name': 'Специализация',
                'verbose_name_plural': 'Специализации',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('skills', models.TextField()),
                ('description', models.TextField()),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('published_at', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.company')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.specialty')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]
