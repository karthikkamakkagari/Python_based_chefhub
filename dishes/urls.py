from django.urls import path
from . import views

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('add/', views.add_dish, name='add_dish'),
    path('edit/<int:pk>/', views.edit_dish, name='edit_dish'),
    path('delete/<int:pk>/', views.delete_dish, name='delete_dish'),
    path('export/', views.export_dishes, name='export_dishes'),
    path('import/', views.import_dishes, name='import_dishes'),
    path('ingredient/<int:pk>/details/', views.ingredient_details, name='ingredient_details'),
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/<int:dish_id>/update-ingredients/', views.update_dish_ingredients, name='update_dish_ingredients'),
]
