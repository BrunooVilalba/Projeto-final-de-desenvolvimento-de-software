# 🚀 EstudaAI - Guia de Início Rápido

## ⚡ Instalação em 5 Minutos

### 1. Pré-requisitos
- Python 3.8+
- PostgreSQL 12+
- Git

### 2. Clone e Configure
```bash
git clone <seu-repositorio>
cd Projeto-final-de-desenvolvimento-de-software
```

### 3. Instalação Automática
```bash
python setup.py
```

### 4. Configure a Chave da OpenAI
Edite o arquivo `.env`:
```env
OPENAI_API_KEY=sua_chave_aqui
```

### 5. Execute o Servidor
```bash
python manage.py runserver
```

### 6. Acesse a Aplicação
Abra: http://127.0.0.1:8000

**Login padrão:**
- Usuário: `admin`
- Senha: `admin123`

## 🎯 Funcionalidades Principais

### ✅ Trilhas Pré-definidas
- 5 categorias de conhecimento
- Trilhas curadas por especialistas
- Diferentes níveis de dificuldade

### ✅ Trilhas Personalizadas com IA
- Descreva seus objetivos
- IA cria trilha personalizada
- Baseada em OpenAI GPT-3.5

### ✅ Acompanhamento de Progresso
- Dashboard com estatísticas
- Marcar etapas como concluídas
- Histórico de estudos

### ✅ Chat com IA
- Dúvidas sobre trilhas
- Sugestões personalizadas
- Suporte 24/7

## 🛠️ Comandos Úteis

```bash
# Executar testes
python test_setup.py

# Popular dados iniciais
python manage.py populate_data

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar migrações
python manage.py migrate
```

## 🐳 Docker (Opcional)

```bash
# Desenvolvimento
docker-compose -f docker-compose.dev.yml up -d

# Produção
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Documentação Completa

- [README.md](README.md) - Documentação principal
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir
- [FAQ.md](FAQ.md) - Perguntas frequentes
- [ROADMAP.md](ROADMAP.md) - Planejamento futuro

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/estudaai/estudaai/issues)
- **Discord**: [Comunidade](https://discord.gg/estudaai)
- **Email**: suporte@estudaai.com

## 🎉 Pronto!

Agora você tem um sistema completo de trilhas de aprendizagem com IA funcionando! Explore as funcionalidades e comece sua jornada de aprendizado personalizada.
