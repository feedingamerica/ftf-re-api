from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet)
router.register(r'run_types', views.RunTypeViewSet)
router.register(r'timeframe_types', views.TimeframeTypeViewSet)
router.register(r'report_scopes', views.ReportScopeViewSet)
router.register(r'control_types', views.ControlTypeViewSet)
router.register(r'reporting_dictionaries', views.ReportingDictionaryViewSet)
router.register(r'report_schedules', views.ReportScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
