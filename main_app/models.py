from django.db import models


class MediaContent(models.Model):
    file = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='Медиа файл')

    class Meta:
        abstract = True


class DataContent(models.Model):
    data = models.TextField(blank=True, verbose_name='Данные')

    class Meta:
        abstract = True


class MenuNavigation(MediaContent):
    heading = models.CharField(max_length=50, verbose_name='Название')
    first_menu = models.CharField(max_length=25, verbose_name='Первый пункт меню')
    second_menu = models.CharField(max_length=25, verbose_name='Второй пункт меню')
    third_menu = models.CharField(max_length=25, verbose_name='Третий пункт меню')
    fourth_menu = models.CharField(max_length=25, verbose_name='Четвертый пункт меню')
    fifth_menu = models.CharField(max_length=25, verbose_name='Пятый пункт меню')
    sixth_menu = models.CharField(max_length=25, verbose_name='Шестой пункт меню')
    creator = models.CharField(max_length=100, verbose_name='Создатель')


class PageContent(MediaContent):
    description = models.TextField(blank=True, verbose_name='Описание')

 
class StatisticalData(DataContent):
    salary_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График зарплат')
    vacancy_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График вакансий')


class RegionalStatistics(DataContent):
    city_salary_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График зарплат по городам')
    city_vacancy_share_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График доли вакансий')


class SkillAnalysis(DataContent):
    dataset_name = models.CharField(max_length=50, verbose_name='Название данных')
    skill_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График навыков')


class JobPost(models.Model):
    headline = models.CharField(max_length=150, verbose_name='Заголовок вакансии')
    details = models.TextField(blank=False, verbose_name='Детали', max_length=255)
