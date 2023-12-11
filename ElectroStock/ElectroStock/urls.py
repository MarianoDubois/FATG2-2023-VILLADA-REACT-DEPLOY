from django.contrib import admin
from django.urls import path, include
from ElectroStockApp import views
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('docs/', include_docs_urls(title="API DOCUMENTATION")),
    path('auth/', include("LoginApp.urls")),
    path("notifications/", include("notifications.urls")),
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

handler404 = 'ElectroStockApp.views.handler_404'