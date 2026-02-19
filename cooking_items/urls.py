from django.urls import path
from . import views

urlpatterns = [
    path('cooking_items/', views.cooking_item_list, name='cooking_item_list'),
    path('cooking_items/add/', views.add_cooking_item, name='cooking_item_add'),
    path('cooking_items/edit/<int:pk>/', views.edit_cooking_item, name='cooking_item_edit'),
    path('cooking_items/delete/<int:pk>/', views.delete_cooking_item, name='cooking_item_delete'),
    path('cooking_items/export/', views.export_cooking_items, name='export_cooking_items'),
    path('cooking_items/import/', views.import_cooking_items, name='import_cooking_items'),
    path('dashboard/', views.dashboard_cooking_item_count, name='dashboard'),

]
