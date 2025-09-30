from django.contrib import admin
from django.urls import path, include
from customers.views import home, dashboard, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ingredients.urls')),
    path('accounts/', include('accounts.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('customers/', include('customers.urls')),
    path('dishes/', include('dishes.urls')),
    path('cooking_items/', include('cooking_items.urls')),
    path('', home, name='home'),  # Home page
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard page
    path('logout/', logout_view, name='logout'),
]

# 👇 Add this for serving images in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
