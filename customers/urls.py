from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.customer_list, name='customer_list'),   # ✅ Added
    path('add/', views.add_customer, name='add_customer'),
    path('generate/<str:customer_id>/', views.generate_ingredient_list, name='generate_ingredient_list'),
    path('download_pdf/<str:customer_id>/', views.download_pdf, name='download_pdf'),
]
