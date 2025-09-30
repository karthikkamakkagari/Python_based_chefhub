from django.urls import path
from . import views

urlpatterns = [
    path('', views.cooking_item_list, name='cooking_item_list'),
    path('add/', views.add_cooking_item, name='cooking_item_add'),   # ✅ consistent
    path('edit/<int:pk>/', views.edit_cooking_item, name='cooking_item_edit'),  # ✅
    path('delete/<int:pk>/', views.delete_cooking_item, name='cooking_item_delete'),  # ✅
]
