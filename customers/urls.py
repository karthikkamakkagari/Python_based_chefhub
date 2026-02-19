from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),

    path('customers/add/', views.customer_add_edit, name='customer_add'),
    path('customers/edit/<int:pk>/', views.customer_add_edit, name='customer_edit'),

    path('delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    path('generate/<int:customer_id>/', views.generate_ingredient_list, name='generate_ingredient_list'),
    path('customers/pdf/<int:customer_id>/', views.export_customer_pdf, name='download_pdf'),

    path('export/<int:customer_id>/', views.export_customer_pdf, name='export_customer_pdf'),

    path('customers/import/', views.import_customers, name='import_customers'),
    path('customers/export/', views.export_customers, name='export_customers'),

    path('dish/add/', views.dish_add, name='dish_add'),
    path('cooking-item/add/', views.cooking_item_add, name='cooking_item_add'),
    path('ingredient/add/', views.ingredient_item_add, name='ingredient_item_add'),
]


