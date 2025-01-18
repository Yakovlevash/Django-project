from django.urls import path
from .views import *

urlpatterns = [
    path('', LandingPage.as_view(), name='home'),
    path('all/', GeneralPageView.as_view(), name='general'),
    path('trends/', TrendsPage.as_view(), name='relevance'),
    path('regional/', RegionalPage.as_view(), name='geography'),
    path('skills/', SkillsPage.as_view(), name='abilitys')
]
