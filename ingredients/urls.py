from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_ingredient_count, name='dashboard'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredient/add/', views.add_edit_ingredient, name='add_ingredient'),
    path('ingredient/edit/<int:pk>/', views.add_edit_ingredient, name='edit_ingredient'),
    path('ingredient/delete/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),
    path('ingredient/export/', views.export_ingredients, name='export_ingredients'),
    path('ingredient/import/', views.import_ingredients, name='import_ingredients'),
]
