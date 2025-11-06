# Projeto-final-de-desenvolvimento-de-software

<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

## EstudaAI - Sistema de Trilhas de Aprendizagem Personalizadas

Sistema web para criação e gerenciamento de trilhas de aprendizagem personalizadas usando React, TypeScript, Vite e Gemini AI.

### [Modelagem] Caso de Uso - Visualizar trilha e progresso
https://miro.com/app/board/uXjVJC1hrHg=/

### [Modelagem] Caso de Uso - Solicitar trilha personalizada via LLM
Link LLM Gemini: https://g.co/gemini/share/7cfa8456d500

Link Diagrama Miro: https://miro.com/app/board/uXjVJC2ENuY=/?share_link_id=829155832950

### [Modelagem] Caso de Uso - Escolher trilha pré-definida.
https://miro.com/app/board/uXjVJChIDBE=/?share_link_id=786603644238

### [Modelagem] Criar o modelo de domínio conceitual do sistema
https://miro.com/app/board/uXjVJ8uKHH0=/

### [Modelagem] Criar o diagrama de conceitual (UML)
https://miro.com/welcomeonboard/ZmdkVkE5a1FsRzREa1krbGxweE1EUkZvMndwRkFmSStVNEVNVHFJdTZ3bUVaemEwR3kweVJmZXIwWElQTGZETWFjaEFFMVhPb0cwOHB3Z1QvOXRwSG5wdWFkdEI4ejVvN3p4di9SVFF4eWY1UDVFWTlpMGROeGNEbG1mUTk4WDdBS2NFMDFkcUNFSnM0d3FEN050ekl3PT0hdjE=?share_link_id=60071469457

## Frontend - EstudaAI (React + Vite + TypeScript)

### Pré-requisitos
- Node.js (versão 18 ou superior)
- npm ou yarn

### Como rodar o frontend

1. Instalar dependências:
```bash
npm install
```

2. Configurar chave da API Gemini:
   - Copie o arquivo `.env.example` para `.env.local` (se existir)
   - Ou configure a variável `GEMINI_API_KEY` no arquivo `services/geminiService.ts`
   - **Nota:** Por segurança, mova a API key para variáveis de ambiente em produção

3. Rodar o servidor de desenvolvimento:
```bash
npm run dev
```

4. Acessar no navegador:
   - Local: http://localhost:3000
   - O servidor Vite pode usar outra porta se a 3000 estiver em uso

### Funcionalidades

- ✅ Landing Page com apresentação do sistema
- ✅ Autenticação de usuários (Login/Registro)
- ✅ Dashboard com trilhas de aprendizagem
- ✅ Criação de trilhas personalizadas com IA (Gemini)
- ✅ Recomendações de trilhas baseadas no perfil do usuário
- ✅ Acompanhamento de progresso
- ✅ Interface responsiva com Tailwind CSS

## Backend - Django (Opcional)

### Como configurar o ambiente e rodar o projeto Django

### 1. Criar o ambiente virtual

No terminal, dentro da pasta raiz do projeto, rode:
```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual
No Windows:
```bash
.\venv\Scripts\activate
```

No Linux/macOS:
```bash
source venv/bin/activate
```

### 3. Instalar as dependências

Instale as dependências listadas no arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

### 4. Rodar o servidor de desenvolvimento

Inicie o servidor Django:
```bash
python manage.py runserver
```

### 5. Depois abra seu navegador e acesse:
http://127.0.0.1:8000/

## Tecnologias Utilizadas

### Frontend
- React 19
- TypeScript
- Vite
- Tailwind CSS
- Google Gemini AI

### Backend (Django)
- Python
- Django
- SQLite

## Estrutura do Projeto

```
├── components/          # Componentes React
│   ├── AuthModal.tsx
│   ├── Dashboard.tsx
│   ├── LandingPage.tsx
│   └── ...
├── services/            # Serviços (API Gemini)
│   └── geminiService.ts
├── types.ts             # Tipos TypeScript
├── App.tsx              # Componente principal
├── index.tsx            # Ponto de entrada
└── vite.config.ts       # Configuração do Vite
```

## Contribuidores

- @Gabriel-Apolinario01
- @BRUNEBAS001
- @Aruak-Malta
- @Felipenar-x
- @Nicleo1112
- @escobarfelipe21
