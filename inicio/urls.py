from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.pagina_cadastro, name='cadastro'),
    path('api/login/', views.api_login, name='api_login'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.logout_view, name='logout'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
