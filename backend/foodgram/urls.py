from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from recipes.views import RecipeUrlViewSet

urlpatterns = [
    path('s/<str:short_link>',
         RecipeUrlViewSet.as_view({'get': 'retrieve',
                                   'patch': 'partial_update',
                                   'delete': 'destroy'})),
    path('api/admin/', admin.site.urls),
    path('api/', include('recipes.urls')),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)