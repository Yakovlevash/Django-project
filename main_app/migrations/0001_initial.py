# Generated by Django 5.1.4 on 2025-01-11 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=150, verbose_name='Заголовок вакансии')),
                ('details', models.TextField(max_length=255, verbose_name='Детали')),
            ],
        ),
        migrations.CreateModel(
            name='MenuNavigation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='Медиа файл')),
                ('heading', models.CharField(max_length=50, verbose_name='Название')),
                ('menu_items', models.JSONField(default=dict, verbose_name='Пункты меню')),
                ('creator', models.CharField(max_length=100, verbose_name='Создатель')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='Медиа файл')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegionalStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, verbose_name='Данные')),
                ('city_salary_chart', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='График зарплат по городам')),
                ('city_vacancy_share_chart', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='График доли вакансий')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SkillAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, verbose_name='Данные')),
                ('dataset_name', models.CharField(max_length=50, verbose_name='Название данных')),
                ('skill_chart', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='График навыков')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatisticalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, verbose_name='Данные')),
                ('salary_chart', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='График зарплат')),
                ('vacancy_chart', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='График вакансий')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
