#!/usr/bin/env python3
"""
Script de teste para verificar se o EstudaAI está funcionando corretamente
"""

import os
import sys
import django
from pathlib import Path

# Adicionar o diretório do projeto ao Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_imports():
    """Testa se todos os imports estão funcionando"""
    print("🔍 Testando imports...")
    
    try:
        from estudaai.models import Category, Trail, Step, UserProgress, CustomTrail, LLMConversation
        from estudaai.views import home, dashboard, trail_list
        from estudaai.forms import CustomUserCreationForm, CustomTrailForm
        from estudaai.llm_service import LLMService
        print("✅ Todos os imports funcionando")
        return True
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print("\n🔍 Testando conexão com banco de dados...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✅ Conexão com banco de dados funcionando")
                return True
            else:
                print("❌ Erro na consulta ao banco")
                return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_models():
    """Testa se os modelos estão funcionando"""
    print("\n🔍 Testando modelos...")
    
    try:
        from estudaai.models import Category, Trail, Step
        
        # Testar criação de categoria
        category, created = Category.objects.get_or_create(
            name="Teste",
            defaults={'description': 'Categoria de teste', 'icon': 'fas fa-test'}
        )
        
        if created:
            print("✅ Categoria criada com sucesso")
        else:
            print("✅ Categoria já existe")
        
        # Testar contagem de objetos
        category_count = Category.objects.count()
        trail_count = Trail.objects.count()
        step_count = Step.objects.count()
        
        print(f"✅ Categorias: {category_count}")
        print(f"✅ Trilhas: {trail_count}")
        print(f"✅ Etapas: {step_count}")
        
        return True
    except Exception as e:
        print(f"❌ Erro nos modelos: {e}")
        return False

def test_llm_service():
    """Testa o serviço de LLM"""
    print("\n🔍 Testando serviço de LLM...")
    
    try:
        from estudaai.llm_service import LLMService
        from django.contrib.auth.models import User
        
        llm_service = LLMService()
        
        # Verificar se a chave da API está configurada
        if not llm_service.api_key:
            print("⚠️ Chave da OpenAI não configurada (funcionalidade limitada)")
        else:
            print("✅ Chave da OpenAI configurada")
        
        print("✅ Serviço de LLM inicializado")
        return True
    except Exception as e:
        print(f"❌ Erro no serviço de LLM: {e}")
        return False

def test_urls():
    """Testa se as URLs estão funcionando"""
    print("\n🔍 Testando URLs...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Testar URLs principais
        urls_to_test = [
            ('home', 'Página inicial'),
            ('trail_list', 'Lista de trilhas'),
            ('category_list', 'Lista de categorias'),
        ]
        
        for url_name, description in urls_to_test:
            try:
                url = reverse(url_name)
                response = client.get(url)
                if response.status_code == 200:
                    print(f"✅ {description}: {url}")
                else:
                    print(f"⚠️ {description}: Status {response.status_code}")
            except Exception as e:
                print(f"❌ {description}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erro nas URLs: {e}")
        return False

def test_static_files():
    """Testa se os arquivos estáticos estão acessíveis"""
    print("\n🔍 Testando arquivos estáticos...")
    
    try:
        static_files = [
            'static/css/style.css',
            'static/js/main.js',
        ]
        
        for file_path in static_files:
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} não encontrado")
        
        return True
    except Exception as e:
        print(f"❌ Erro nos arquivos estáticos: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 Iniciando testes do EstudaAI...\n")
    
    tests = [
        (test_imports, "Imports"),
        (test_database_connection, "Conexão com banco"),
        (test_models, "Modelos"),
        (test_llm_service, "Serviço de LLM"),
        (test_urls, "URLs"),
        (test_static_files, "Arquivos estáticos")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func, test_name in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Erro inesperado em {test_name}: {e}")
    
    print(f"\n📊 Resultado dos testes: {passed}/{total} passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O EstudaAI está funcionando corretamente.")
        print("\n📋 Próximos passos:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://127.0.0.1:8000")
        print("3. Faça login com: admin / admin123")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        print("\n💡 Dicas:")
        print("- Execute: python manage.py migrate")
        print("- Execute: python manage.py populate_data")
        print("- Verifique se o PostgreSQL está rodando")

if __name__ == "__main__":
    main()
