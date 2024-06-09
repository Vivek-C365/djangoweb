from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import Http404

# Custom view for handling dynamic URLs
def dynamic_view(request, dynamic_part):
    # Example logic: Render the template if the dynamic part meets a condition
    # Replace this with your actual logic
    if dynamic_part:  # Replace with your condition
        return TemplateView.as_view(template_name='index.html')(request)
    else:
        raise Http404("Page not found")

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # Dynamic URL handling
    path('<str:dynamic_part>/', dynamic_view, name='dynamic_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
