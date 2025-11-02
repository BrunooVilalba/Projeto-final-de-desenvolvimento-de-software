.PHONY: help install setup run test clean migrate collectstatic createsuperuser populate

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências
	pip install -r requirements.txt

setup: ## Configura o projeto completo
	python setup.py

run: ## Executa o servidor de desenvolvimento
	python manage.py runserver

test: ## Executa os testes
	python test_setup.py

clean: ## Limpa arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/

migrate: ## Executa as migrações
	python manage.py makemigrations
	python manage.py migrate

collectstatic: ## Coleta arquivos estáticos
	python manage.py collectstatic --noinput

createsuperuser: ## Cria um superusuário
	python manage.py createsuperuser

populate: ## Popula o banco com dados iniciais
	python manage.py populate_data

shell: ## Abre o shell do Django
	python manage.py shell

dbshell: ## Abre o shell do banco de dados
	python manage.py dbshell

docker-build: ## Constrói a imagem Docker
	docker build -t estudaai .

docker-run: ## Executa o container Docker
	docker-compose up -d

docker-stop: ## Para o container Docker
	docker-compose down

docker-logs: ## Mostra os logs do container
	docker-compose logs -f

docker-dev: ## Executa em modo de desenvolvimento com Docker
	docker-compose -f docker-compose.dev.yml up -d

docker-dev-stop: ## Para o ambiente de desenvolvimento
	docker-compose -f docker-compose.dev.yml down

format: ## Formata o código com Black
	black .

lint: ## Executa o linter
	flake8 .

check: ## Executa todas as verificações
	black --check .
	flake8 .
	python test_setup.py

deploy: ## Deploy para produção (ajustar conforme necessário)
	@echo "Deploy não configurado. Configure conforme sua infraestrutura."
