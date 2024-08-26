from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .routers import *
from scientist.views import *

# Swagger schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Scientist API",
        default_version='v1',
        description="API для управления данными ученых",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dm1tryace@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# router = MyCustomRouter()
# router.register(r'scientist', ScientistViewSet, basename='scientist')
# print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    # JWT
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/scientist/', ScientistAPIList.as_view(), name='scientist_list'),
    path('api/v1/scientist/<int:pk>/', ScientistAPIUpdate.as_view(), name='scientist_update'),
    path('api/v1/scientistdelete/<int:pk>/', ScientistAPIDestroy.as_view(), name='scientist_delete'),

    # Swagger UI and Redoc UI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
        
    #path('api/v1/', include(router.urls)) # http://127.0.0.1:8000/api/v1/scientist/
    
    #path('api/v1/scientistlist/', ScientistViewSet.as_view({'get': 'list'})), # маршрутом подразумеваем только чтение
    #path('api/v1/scientistlist/<int:pk>/', ScientistViewSet.as_view({'put': 'update'})), # а здесь изменение т.к указали pk, такая вещь автоматизирована роутерами
    
    #path('api/v1/scientistlist/', ScientistAPIList.as_view()),
    #path('api/v1/scientistlist/<int:pk>/', ScientistAPIUpdate.as_view()),
    #path('api/v1/scientistdetail/<int:pk>/', ScientistAPIDetailView.as_view()),
]
