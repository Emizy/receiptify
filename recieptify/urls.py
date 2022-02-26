"""agroconet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from recieptify import routes
from recieptify import settings
from apps.core.views import test
schema_view = get_schema_view(
    openapi.Info(
        title="RECEIPTIFY API",
        default_version="v1",
        description="Endpoints showing interactable part of the system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@receiptify.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(SessionAuthentication, JWTAuthentication),
    permission_classes=(permissions.IsAdminUser, permissions.IsAuthenticated),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("v1/api/", include(routes.router.urls)),
    path("test/", test),

    path("",
         schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui",
         ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
