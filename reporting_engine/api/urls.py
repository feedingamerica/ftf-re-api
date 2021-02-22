from django.urls import path
from . import views

urlpatterns = [
    path('report_schedule/', views.report_schedule, name = 'report_schedule')
]
