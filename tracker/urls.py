from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add/', views.add_complaint_view, name='add_complaint'),
    path('portal/login/', views.admin_login_view, name='admin_login'),
    path('portal/dashboard/', views.custom_admin_dashboard, name='admin_dashboard'),
    path('portal/logout/', views.admin_logout_view, name='admin_logout'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
    path('admin-portal/', views.admin_login_view, name='admin_login'),
    path('admin-portal/dashboard/', views.custom_admin_dashboard, name='admin_dashboard'),
    path('admin-portal/logout/', views.admin_logout_view, name='admin_logout'),
]