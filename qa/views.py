from django.shortcuts import render
from django.views.generic import View
from .models import *


class AbstractView(View):
    template = None
    data_model = None
    context_key = None

    def fetch_data(self):
        return self.data_model.objects.all() if self.data_model else []

    def prepare_context(self, **extra_context):
        return {
            self.context_key: self.fetch_data(),
            **extra_context,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template, self.prepare_context())


class LandingPage(AbstractView):
    template = "index.html"
    data_model = PageContent
    context_key = 'content'

class TrendsPage(AbstractView):
    template = "relevance.html"
    data_model = StatisticalData 
    context_key = 'statistics'

class RegionalPage(AbstractView):
    template = "geography.html"
    data_model = RegionalStatistics
    context_key = 'region_data'

class SkillsPage(AbstractView):
    template = "skills.html"
    data_model = SkillAnalysis
    context_key = 'skills_analysis'

class GeneralPageView(AbstractView):
    template_name = "statistic.html"

    def get(self, request, *args, **kwargs):
        statistics = self.fetch_data()
        return render(request, self.template_name, self.prepare_context())
    