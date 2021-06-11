# Generated by Django 3.2.2 on 2021-06-09 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancies', '0007_alter_application_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('status', models.CharField(choices=[('Не ищу работу', 'Not In Search'),
                                                     ('Рассматриваю предложения', 'Consideration'),
                                                     ('Ищу работу', 'In Search')],
                                            default='Ищу работу',
                                            max_length=32)),
                ('salary', models.IntegerField()),
                ('grade', models.CharField(choices=[('intern', 'Intern'),
                                                    ('junior', 'Junior'),
                                                    ('middle', 'Middle'),
                                                    ('senior', 'Senior'),
                                                    ('lead', 'Lead')],
                                           default='junior',
                                           max_length=32)),
                ('education', models.TextField()),
                ('experience', models.TextField()),
                ('portfolio', models.URLField()),
                ('specialty', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                   to='vacancies.specialty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
