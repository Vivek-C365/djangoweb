from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Custom view for handling dynamic URLs
def dynamic_view(request, dynamic_part):
    return TemplateView.as_view(template_name='index.html')(request)  # Example response, replace with your logic

# Swagger schema view configuration
schema_view = get_schema_view(
   openapi.Info(
      title="Certscope",
      default_version='v1'
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Dynamic URL handling
    path('<str:dynamic_part>/', dynamic_view, name='dynamic_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
