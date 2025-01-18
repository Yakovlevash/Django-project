from django.contrib import admin
from .models import *

admin.site.register([
    PageContent,
    StatisticalData,
    RegionalStatistics,
    SkillAnalysis
])
