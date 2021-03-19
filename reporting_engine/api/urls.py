from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('reports', views.ReportViewSet, name='reports'),
    path('report_schedules', views.report_schedule, name='report_schedules'),
    path('run_types', views.RunTypeViewSet, name='run_types'),
    path('timeframe_types', views.TimeframeTypeViewSet, name='timeframe_types'),
    path('report_scopes', views.ReportScopeViewSet, name='report_scopes'),
    path('control_types', views.ControlTypeViewSet, name='control_types'),
    path('reporting_dictionaries', views.ReportingDictionaryViewSet, name='reporting_dictionaries'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
