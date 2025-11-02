#!/usr/bin/env python3
"""
Script de configuração do EstudaAI
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Adicionar o diretório do projeto ao Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}:")
        print(e.stderr)
        return False

def check_postgresql():
    """Verifica se o PostgreSQL está instalado e rodando"""
    print("\n🔍 Verificando PostgreSQL...")
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL não encontrado")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL não está instalado")
        return False

def create_database():
    """Cria o banco de dados se não existir"""
    print("\n🗄️ Criando banco de dados...")
    
    # Configurações do banco
    db_name = os.getenv('DB_NAME', 'estudaai')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    
    # Comando para criar o banco
    create_db_cmd = f"""
    PGPASSWORD={db_password} psql -U {db_user} -h localhost -c "CREATE DATABASE {db_name};" 2>/dev/null || echo "Banco já existe ou erro na criação"
    """
    
    if run_command(create_db_cmd, "Criando banco de dados"):
        print(f"✅ Banco de dados '{db_name}' configurado")
        return True
    return False

def install_requirements():
    """Instala as dependências do Python"""
    return run_command("pip install -r requirements.txt", "Instalando dependências Python")

def run_migrations():
    """Executa as migrações do Django"""
    return run_command("python manage.py makemigrations", "Criando migrações") and \
           run_command("python manage.py migrate", "Aplicando migrações")

def create_superuser():
    """Cria um superusuário se não existir"""
    print("\n👤 Verificando superusuário...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@estudaai.com',
                password='admin123',
                first_name='Administrador',
                last_name='EstudaAI'
            )
            print("✅ Superusuário 'admin' criado (senha: admin123)")
        else:
            print("✅ Superusuário já existe")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def populate_initial_data():
    """Popula o banco com dados iniciais"""
    return run_command("python manage.py populate_data", "Populando dados iniciais")

def collect_static():
    """Coleta arquivos estáticos"""
    return run_command("python manage.py collectstatic --noinput", "Coletando arquivos estáticos")

def main():
    """Função principal de configuração"""
    print("🚀 Iniciando configuração do EstudaAI...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('manage.py'):
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Verificar PostgreSQL
    if not check_postgresql():
        print("\n📋 Para instalar o PostgreSQL:")
        print("  macOS: brew install postgresql")
        print("  Ubuntu: sudo apt install postgresql postgresql-contrib")
        print("  Windows: Baixe do site oficial do PostgreSQL")
        print("\nApós instalar, execute este script novamente.")
        sys.exit(1)
    
    # Criar arquivo .env se não existir
    if not os.path.exists('.env'):
        print("\n📝 Criando arquivo .env...")
        env_content = """# Database Configuration
DB_NAME=estudaai
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Django Configuration
SECRET_KEY=django-insecure-_2o)1w%&5fkyf)g0ut+3031_290#e(n65unhfb1()@up+m$&x=
DEBUG=True
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado")
        print("⚠️  Configure sua chave da OpenAI no arquivo .env")
    
    # Executar etapas de configuração
    steps = [
        (install_requirements, "Instalação de dependências"),
        (create_database, "Configuração do banco de dados"),
        (run_migrations, "Migrações do Django"),
        (create_superuser, "Criação do superusuário"),
        (populate_initial_data, "População de dados iniciais"),
        (collect_static, "Coleta de arquivos estáticos")
    ]
    
    success_count = 0
    for step_func, description in steps:
        if step_func():
            success_count += 1
        else:
            print(f"❌ Falha na etapa: {description}")
            break
    
    if success_count == len(steps):
        print("\n🎉 Configuração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Configure sua chave da OpenAI no arquivo .env")
        print("2. Execute: python manage.py runserver")
        print("3. Acesse: http://127.0.0.1:8000")
        print("4. Faça login com: admin / admin123")
    else:
        print(f"\n⚠️  Configuração parcialmente concluída ({success_count}/{len(steps)} etapas)")
        print("Verifique os erros acima e execute novamente se necessário.")

if __name__ == "__main__":
    main()
