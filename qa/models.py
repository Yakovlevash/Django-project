from django.db import models


class MediaContent(models.Model):
    file = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='Медиа файл')

    class Meta:
        abstract = True


class DataContent(models.Model):
    data = models.TextField(blank=True, verbose_name='Данные')

    class Meta:
        abstract = True
        

class PageContent(MediaContent):
    description = models.TextField(blank=True, verbose_name='Описание')

 
class StatisticalData(DataContent):
    salary_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График зарплат')
    vacancy_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График вакансий')


class RegionalStatistics(DataContent):
    city_salary_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График зарплат по городам')
    city_vacancy_share_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График доли вакансий')


class SkillAnalysis(DataContent):
    skill_chart = models.ImageField(upload_to='media/%Y/%m/%d', blank=False, verbose_name='График навыков')
