from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
