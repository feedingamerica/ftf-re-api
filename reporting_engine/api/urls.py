from django.urls import path
from . import views

urlpatterns = [
    path('report_schedules', views.report_schedule, name = 'report_schedule'),
    path('test-api-key', views.test_api_key, name='test_api_key'),
    path('test-admin-token-auth', views.test_admin_token_auth, name='test_admin_token_auth'),

]
