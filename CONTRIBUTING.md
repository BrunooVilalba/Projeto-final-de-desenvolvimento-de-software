# Guia de Contribuição

Obrigado por considerar contribuir para o EstudaAI! Este documento fornece diretrizes para contribuir com o projeto.

## Como Contribuir

### 1. Fork e Clone
1. Faça um fork do repositório
2. Clone seu fork localmente:
   ```bash
   git clone https://github.com/seu-usuario/Projeto-final-de-desenvolvimento-de-software.git
   cd Projeto-final-de-desenvolvimento-de-software
   ```

### 2. Configurar Ambiente
1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou
   venv\Scripts\activate     # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados:
   ```bash
   python setup.py
   ```

### 3. Criar Branch
```bash
git checkout -b feature/nome-da-feature
# ou
git checkout -b bugfix/descricao-do-bug
```

### 4. Fazer Mudanças
- Faça suas mudanças no código
- Adicione testes se necessário
- Atualize a documentação se necessário

### 5. Testar
```bash
# Executar testes
python test_setup.py

# Verificar estilo de código
flake8 .

# Formatar código
black .
```

### 6. Commit
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
# ou
git commit -m "fix: corrige bug na autenticação"
```

### 7. Push e Pull Request
```bash
git push origin feature/nome-da-feature
```

Depois, abra um Pull Request no GitHub.

## Padrões de Código

### Python
- Siga o PEP 8
- Use Black para formatação
- Use type hints quando apropriado
- Escreva docstrings para funções e classes

### Django
- Siga as convenções do Django
- Use nomes descritivos para views e URLs
- Documente modelos e campos

### Frontend
- Use Bootstrap 5 para componentes
- Mantenha CSS organizado
- Use JavaScript moderno (ES6+)

## Convenções de Commit

Use o formato:
```
tipo: descrição breve

Descrição mais detalhada se necessário

Fixes #123
```

Tipos:
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `style`: formatação
- `refactor`: refatoração
- `test`: testes
- `chore`: tarefas de manutenção

## Estrutura do Projeto

```
estudaai/
├── models.py          # Modelos de dados
├── views.py           # Views da aplicação
├── urls.py            # URLs
├── forms.py           # Formulários
├── admin.py           # Configuração do admin
├── llm_service.py     # Serviço de IA
└── templates/         # Templates HTML
```

## Testes

### Executar Testes
```bash
python test_setup.py
```

### Adicionar Novos Testes
- Testes unitários para funções
- Testes de integração para views
- Testes de modelo para validações

## Documentação

- Atualize o README.md se necessário
- Documente novas funcionalidades
- Mantenha exemplos atualizados

## Issues

### Reportar Bugs
Use o template de bug report e inclua:
- Descrição clara do problema
- Passos para reproduzir
- Ambiente (OS, Python, Django)
- Screenshots se aplicável

### Sugerir Funcionalidades
Use o template de feature request e inclua:
- Descrição da funcionalidade
- Caso de uso
- Alternativas consideradas

## Pull Requests

### Antes de Enviar
- [ ] Código segue os padrões
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Commit messages claros
- [ ] Branch atualizada com main

### Processo de Review
1. Mantenedores revisam o código
2. Sugestões de melhoria são feitas
3. Contribuidor faz ajustes se necessário
4. PR é aprovado e mergeado

## Comunicação

- Use issues para discussões
- Seja respeitoso e construtivo
- Ajude outros contribuidores
- Siga o código de conduta

## Reconhecimento

Contribuidores serão reconhecidos no README e releases.

## Dúvidas?

Abra uma issue ou entre em contato com os mantenedores.

Obrigado por contribuir! 🎉
