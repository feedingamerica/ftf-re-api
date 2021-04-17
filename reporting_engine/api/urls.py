from django.urls import include, path, re_path
from . import views
from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
	openapi.Info(
		title='Swagger',
		default_version='v2',
		description='Welcome to Swagger',
		),
	public=True,
	permission_classes=(permissions.IsAuthenticated, ),
	)

router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet)
router.register(r'run_types', views.RunTypeViewSet)
router.register(r'timeframe_types', views.TimeframeTypeViewSet)
router.register(r'report_scopes', views.ReportScopeViewSet)
router.register(r'control_types', views.ControlTypeViewSet)
router.register(r'reporting_dictionaries', views.ReportingDictionaryViewSet)
router.register(r'report_schedules', views.ReportScheduleViewSet)


urlpatterns = [
	re_path(r'^doc(?P<format>\.json|\.yaml)$', 
		schema_view.without_ui(cache_timeout=0), name='schema-json'),
	path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
		name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
		name='schema-redoc'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reports/<int:report_scope_id>/<int:report_scope_value>/', views.get_reports),
	path('report_options/', views.report_options, name='report-options'),
	path('report_total/<int:report_id>/', views.get_report_total, name='report')
]
