from django.urls import path
from . import views

urlpatterns = [
    path('report_schedules', views.report_schedule, name = 'report_schedule'),
    path('report_options', views.report_options, name = 'report_options'),
    path('reports_totals/<int:report_id>/', views.report_totals, name = 'report_total')

]
