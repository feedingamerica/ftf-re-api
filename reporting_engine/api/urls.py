from django.urls import path
from . import views

urlpatterns = [
    path('report_schedules', views.report_schedule, name = 'report_schedule')
]
