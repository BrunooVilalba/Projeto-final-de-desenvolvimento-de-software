from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard e trilhas
    path('dashboard/', views.dashboard, name='dashboard'),
    path('trails/', views.trail_list, name='trail_list'),
    path('trail/<int:trail_id>/', views.trail_detail, name='trail_detail'),
    path('my-trails/', views.my_trails, name='my_trails'),
    
    # Trilhas personalizadas
    path('create-custom-trail/', views.create_custom_trail, name='create_custom_trail'),
    
    # IA e chat
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    
    # Categorias
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    
    # Ações
    path('enroll-trail/<int:trail_id>/', views.enroll_trail, name='enroll_trail'),
    path('mark-step-complete/<int:step_id>/', views.mark_step_complete, name='mark_step_complete'),
]
