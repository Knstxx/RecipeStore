from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from api.views import recipe_redirect_view

urlpatterns = [
    path('s/<str:short_link>', recipe_redirect_view, name='recipe_redirect'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
