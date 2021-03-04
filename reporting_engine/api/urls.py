from django.urls import path
from . import views

urlpatterns = [
    path('report_schedules', views.report_schedule, name = 'report_schedule'),
    path('test-api-key', views.test_api_key, name='test_api_key'),
    path('test-api-key-and-auth', views.test_api_key_and_auth, name='test_api_key_and_auth'),
    path('test-api-key-or-auth', views.test_api_key_or_auth, name='test_api_key_or_auth')


]
