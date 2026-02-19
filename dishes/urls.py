from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_dish_count, name='dashboard'),
    path('dishes', views.dish_list, name='dish_list'),
    path('dishes/add/', views.add_dish, name='add_dish'),
    
    path('dishes/edit/<int:pk>/', views.edit_dish, name='edit_dish'),
    path('dishes/delete/<int:pk>/', views.delete_dish, name='delete_dish'),
    path('dishes/export/', views.export_dishes, name='export_dishes'),
    path('dishes/import/', views.import_dishes, name='import_dishes'),
    path("dishes/get-ingredient/", views.get_ingredient_details, name="get_ingredient_details"),

]
