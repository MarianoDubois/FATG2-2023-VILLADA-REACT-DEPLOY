"""ElectroStock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from ElectroStockApp import views
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [path("admin/", admin.site.urls),
               path("api/", include("api.urls")),
               path('upload_csv/', views.upload_csv, name='upload_csv'),
               path('docs/', include_docs_urls(title="API DOCUMENTATION")),
               ]


# Ruta para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Ruta para servir archivos estáticos en producción
    urlpatterns += [
        path('media/<path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]   