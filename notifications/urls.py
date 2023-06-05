"""
URL configuration for notifications project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from rest_framework import permissions
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from distribution.views import ClientViewSet, DistributionViewSet, StatisticViewSet


schema_view = get_schema_view(
   openapi.Info(
      title="Notifications Service",
      default_version='v1',
      description="Документация по методам тестового задания",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #url для создание нового клиента
    path('api/client/', ClientViewSet.as_view({'post': 'create'})),
    #url для удаления клиента и обновления его атрибутов
    path('api/client/<int:pk>/', ClientViewSet.as_view({'delete': 'destroy', 'put': 'update'})),

    #url для создания новой рассылки
    path('api/distribution/', DistributionViewSet.as_view({'post': 'create'})),
    #url для удаления, обновления атрибутов рассылки и получения детальной статистики по ней
    path('api/distribution/<int:pk>/', DistributionViewSet.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'})),

    #url для получения общей статистики по рассылкам
    path('api/statistic/', StatisticViewSet.as_view({'get': 'list'})),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #url для просмотра документации по API (5-й пункт дополнительных заданий)
    re_path(r'^swagger/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

