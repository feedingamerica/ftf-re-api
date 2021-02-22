from django.urls import path
from . import views

urlpatterns [
    path('report-schedule/', views.report_schedule, name = 'report_schedule')
]
