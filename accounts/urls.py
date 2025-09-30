from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('signup/', views.signup_view, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('profile/', views.profile_view, name='profile'),
    #  path('user_management/', views.user_management, name='user_management'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
