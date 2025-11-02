# EstudaAI - Sistema de Recomendação de Trilhas de Aprendizagem

O EstudaAI é uma aplicação web voltada para auxiliar estudantes no planejamento de seus estudos por meio da recomendação de trilhas de aprendizagem. O sistema oferece duas formas de utilização: o aluno pode escolher entre trilhas de estudo pré-definidas (curadas por especialistas) ou criar trilhas personalizadas com o auxílio de um agente baseado em LLM (Large Language Model).

## 🚀 Funcionalidades

- **Autenticação de usuários** (login e cadastro)
- **Trilhas pré-definidas** por área de conhecimento
- **Trilhas personalizadas** criadas com IA (OpenAI GPT)
- **Acompanhamento de progresso** nas trilhas
- **Interface de chat com IA** para dúvidas e sugestões
- **Dashboard personalizado** com estatísticas de estudo
- **Sistema administrativo** para gerenciar categorias e trilhas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 4.2+ com Python 3.8+
- **Banco de Dados**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **IA**: OpenAI GPT-3.5-turbo
- **Estilização**: Bootstrap 5, Font Awesome, CSS customizado

## 📋 Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Conta na OpenAI (para funcionalidades de IA)

## ⚡ Instalação Rápida

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Projeto-final-de-desenvolvimento-de-software
```

### 2. Execute o script de configuração automática
```bash
python setup.py
```

O script irá:
- Instalar todas as dependências
- Configurar o banco de dados PostgreSQL
- Executar migrações
- Criar superusuário (admin/admin123)
- Popular dados iniciais
- Coletar arquivos estáticos

### 3. Configure a chave da OpenAI
Edite o arquivo `.env` e adicione sua chave da OpenAI:
```env
OPENAI_API_KEY=sua_chave_aqui
```

### 4. Execute o servidor
```bash
python manage.py runserver
```

### 5. Acesse a aplicação
Abra seu navegador em: http://127.0.0.1:8000/

## 🔧 Instalação Manual

Se preferir instalar manualmente:

### 1. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar PostgreSQL
```bash
# Criar banco de dados
createdb estudaai

# Ou via psql
psql -U postgres -c "CREATE DATABASE estudaai;"
```

### 4. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DB_NAME=estudaai
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
OPENAI_API_KEY=sua_chave_aqui
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
```

### 5. Executar migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Criar superusuário
```bash
python manage.py createsuperuser
```

### 7. Popular dados iniciais
```bash
python manage.py populate_data
```

### 8. Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### 9. Executar servidor
```bash
python manage.py runserver
```

## 📊 Estrutura do Projeto

```
Projeto-final-de-desenvolvimento-de-software/
├── estudaai/                 # Aplicação principal
│   ├── management/           # Comandos de gerenciamento
│   ├── migrations/           # Migrações do banco
│   ├── templates/            # Templates HTML
│   ├── admin.py             # Configuração do admin
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views da aplicação
│   ├── urls.py              # URLs da aplicação
│   ├── forms.py             # Formulários
│   └── llm_service.py       # Serviço de integração com IA
├── mysite/                  # Configurações do Django
│   ├── settings.py          # Configurações
│   └── urls.py              # URLs principais
├── static/                  # Arquivos estáticos
│   ├── css/                 # Estilos CSS
│   ├── js/                  # JavaScript
│   └── images/              # Imagens
├── templates/               # Templates base
├── requirements.txt         # Dependências Python
├── setup.py                 # Script de configuração
└── manage.py               # Gerenciador Django
```

## 🎯 Casos de Uso Implementados

- **UC01** - Login e autenticação do usuário
- **UC02** - Escolher trilha pré-definida
- **UC03** - Solicitar trilha personalizada via LLM
- **UC04** - Visualizar trilha e progresso
- **UC05** - Marcar etapa como concluída
- **UC06** - Gerenciar categorias, trilhas e etapas (Admin)

## 🤖 Integração com IA

O sistema utiliza a API da OpenAI para:
- Gerar trilhas personalizadas baseadas na descrição do usuário
- Responder perguntas sobre trilhas de estudo
- Fornecer sugestões e orientações educacionais

## 👥 Usuários Padrão

Após a instalação, você pode fazer login com:
- **Usuário**: admin
- **Senha**: admin123

## 📱 Interface

A interface é totalmente responsiva e inclui:
- Dashboard com estatísticas de progresso
- Lista de trilhas com filtros e busca
- Visualização detalhada de trilhas com progresso
- Chat interativo com IA
- Sistema de criação de trilhas personalizadas
- Interface administrativa completa

## 🔒 Segurança

- Autenticação segura com Django
- Proteção CSRF em todos os formulários
- Validação de dados em frontend e backend
- Configurações de segurança do Django

## 📈 Próximas Funcionalidades

- [ ] Sistema de certificados
- [ ] Gamificação com pontos e conquistas
- [ ] Integração com calendário
- [ ] Notificações por email
- [ ] API REST para integrações
- [ ] Aplicativo mobile

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através dos issues do GitHub.

---

**Desenvolvido com ❤️ para facilitar o aprendizado através da tecnologia**
