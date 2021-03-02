from django.urls import path
from . import views

urlpatterns = [
    path('report_schedules', views.report_schedule, name = 'report_schedule'),
    path('test-api-auth', views.test_api_auth, name='test_api_auth'),
]
