# Makefile para Top Pet System
# Comandos simplificados para desenvolvimento e testes

.PHONY: help build up down test test-crud clean logs shell migrate

# Variáveis
COMPOSE_FILE = docker-compose.yml
SERVICE_WEB = web
SERVICE_DB = db

help: ## Mostrar esta ajuda
	@echo "Top Pet System - Comandos Disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir containers Docker
	docker-compose build

up: ## Iniciar todos os serviços
	docker-compose up -d
	@echo "✅ Serviços iniciados"
	@echo "🌐 API: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/api/docs/"

down: ## Parar todos os serviços
	docker-compose down

stop: ## Parar serviços sem remover containers
	docker-compose stop

restart: ## Reiniciar serviços
	docker-compose restart

logs: ## Ver logs dos serviços
	docker-compose logs -f

logs-web: ## Ver logs apenas da aplicação web
	docker-compose logs -f $(SERVICE_WEB)

logs-db: ## Ver logs apenas do banco de dados
	docker-compose logs -f $(SERVICE_DB)

shell: ## Acessar shell do container web
	docker-compose exec $(SERVICE_WEB) bash

shell-db: ## Acessar shell do PostgreSQL
	docker-compose exec $(SERVICE_DB) psql -U user -d top_pet_db

migrate: ## Executar migrações do banco
	docker-compose exec $(SERVICE_WEB) python manage.py migrate

makemigrations: ## Criar novas migrações
	docker-compose exec $(SERVICE_WEB) python manage.py makemigrations

superuser: ## Criar superusuário Django
	docker-compose exec $(SERVICE_WEB) python manage.py createsuperuser

collectstatic: ## Coletar arquivos estáticos
	docker-compose exec $(SERVICE_WEB) python manage.py collectstatic --noinput

test: ## Executar testes unitários
	docker-compose exec $(SERVICE_WEB) python manage.py test

test-coverage: ## Executar testes com cobertura
	docker-compose exec $(SERVICE_WEB) coverage run --source='.' manage.py test
	docker-compose exec $(SERVICE_WEB) coverage report
	docker-compose exec $(SERVICE_WEB) coverage html

test-crud: ## Executar simulação CRUD completa
	@echo "🚀 Iniciando simulação CRUD..."
	docker-compose up -d
	@sleep 10
	@echo "⏳ Aguardando serviços ficarem prontos..."
	@timeout 60 bash -c 'until docker-compose exec -T $(SERVICE_DB) pg_isready -U user -d top_pet_db; do sleep 2; done'
	@echo "🗄️ Executando migrações..."
	docker-compose exec -T $(SERVICE_WEB) python manage.py migrate --verbosity=0
	@echo "📊 Executando simulação CRUD..."
	docker-compose exec $(SERVICE_WEB) python test_api_simulation.py
	@echo "📈 Gerando análise..."
	docker-compose exec $(SERVICE_WEB) python analyze_test_report.py

test-crud-ci: ## Executar simulação CRUD para CI (sem interação)
	docker-compose up -d
	@sleep 15
	timeout 60 bash -c 'until docker-compose exec -T $(SERVICE_DB) pg_isready -U user -d top_pet_db; do sleep 2; done'
	docker-compose exec -T $(SERVICE_WEB) python manage.py migrate --verbosity=0
	docker-compose exec -T $(SERVICE_WEB) python test_api_simulation.py
	docker-compose exec -T $(SERVICE_WEB) python analyze_test_report.py

dev-setup: ## Setup completo para desenvolvimento
	@echo "🔧 Configurando ambiente de desenvolvimento..."
	docker-compose build
	docker-compose up -d
	@sleep 10
	@echo "⏳ Aguardando banco ficar pronto..."
	@timeout 60 bash -c 'until docker-compose exec -T $(SERVICE_DB) pg_isready -U user -d top_pet_db; do sleep 2; done'
	docker-compose exec -T $(SERVICE_WEB) python manage.py migrate
	@echo "📝 Criando dados básicos..."
	docker-compose exec -T $(SERVICE_WEB) python -c "import os; import django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings'); django.setup(); from configuracao.models import HorarioFuncionamento; [HorarioFuncionamento.objects.get_or_create(dia_semana=i, defaults={'hora_abertura': '08:00', 'hora_fechamento': '18:00' if i < 6 else '12:00'}) for i in range(1, 7)]"
	@echo "✅ Ambiente pronto!"
	@echo "🌐 API: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/api/docs/"

clean: ## Limpar containers, volumes e imagens
	docker-compose down -v --rmi all
	docker system prune -f

status: ## Mostrar status dos serviços
	docker-compose ps

health: ## Verificar saúde dos serviços
	@echo "🔍 Verificando saúde dos serviços..."
	@docker-compose ps --format table
	@echo ""
	@echo "🐘 PostgreSQL:"
	@docker-compose exec -T $(SERVICE_DB) pg_isready -U user -d top_pet_db && echo "✅ PostgreSQL OK" || echo "❌ PostgreSQL não disponível"
	@echo ""
	@echo "🐍 Django:"
	@curl -s http://localhost:8000/api/ > /dev/null && echo "✅ API OK" || echo "❌ API não disponível"

backup-db: ## Fazer backup do banco de dados
	@echo "💾 Fazendo backup do banco..."
	docker-compose exec -T $(SERVICE_DB) pg_dump -U user top_pet_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup criado: backup_$(shell date +%Y%m%d_%H%M%S).sql"

restore-db: ## Restaurar backup do banco (usage: make restore-db FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then echo "❌ Especifique o arquivo: make restore-db FILE=backup.sql"; exit 1; fi
	@echo "🔄 Restaurando backup: $(FILE)"
	docker-compose exec -T $(SERVICE_DB) psql -U user -d top_pet_db < $(FILE)
	@echo "✅ Backup restaurado"

# Comandos de desenvolvimento rápido
quick-test: up migrate test-crud ## Setup rápido + teste CRUD

quick-dev: dev-setup ## Alias para dev-setup

# Comandos de produção
prod-build: ## Build para produção
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Iniciar em modo produção
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Parar modo produção
	docker-compose -f docker-compose.prod.yml down
