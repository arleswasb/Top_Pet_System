#!/bin/bash
# Script para executar simulação CRUD com Docker Compose
# Usage: ./run_crud_simulation_docker.sh

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}===================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===================================================${NC}\n"
}

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose não está instalado ou não está no PATH"
    exit 1
fi

print_header "🐳 SIMULAÇÃO CRUD TOP PET SYSTEM - DOCKER COMPOSE"

# 1. Parar containers existentes
print_status "Parando containers existentes..."
docker-compose down -v 2>/dev/null || true

# 2. Construir e iniciar containers
print_status "Construindo e iniciando containers..."
docker-compose up -d --build

# 3. Aguardar containers ficarem prontos
print_status "Aguardando containers ficarem prontos..."
sleep 10

# Verificar se containers estão rodando
if ! docker-compose ps | grep -q "Up"; then
    print_error "Containers não estão rodando corretamente"
    docker-compose logs
    exit 1
fi

# 4. Aguardar banco de dados ficar pronto
print_status "Aguardando PostgreSQL ficar pronto..."
timeout 60 bash -c 'until docker-compose exec -T db pg_isready -U user -d top_pet_db; do sleep 2; done'

if [ $? -ne 0 ]; then
    print_error "Timeout aguardando PostgreSQL"
    docker-compose logs db
    exit 1
fi

# 5. Executar migrações
print_status "Executando migrações..."
docker-compose exec -T web python manage.py migrate --verbosity=0

# 6. Criar dados básicos necessários
print_status "Criando dados básicos..."
docker-compose exec -T web python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
django.setup()

from configuracao.models import HorarioFuncionamento

# Criar horários de funcionamento se não existirem
if not HorarioFuncionamento.objects.exists():
    horarios = [
        {'dia_semana': 1, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
        {'dia_semana': 2, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
        {'dia_semana': 3, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
        {'dia_semana': 4, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
        {'dia_semana': 5, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
        {'dia_semana': 6, 'hora_abertura': '08:00', 'hora_fechamento': '12:00'},
    ]
    
    for horario in horarios:
        HorarioFuncionamento.objects.create(**horario)
    
    print('Horários de funcionamento criados')
else:
    print('Horários já existem')
"

# 7. Executar simulação CRUD
print_header "🚀 EXECUTANDO SIMULAÇÃO CRUD"
docker-compose exec web python test_api_simulation.py

# 8. Analisar resultados
print_header "📊 ANÁLISE DOS RESULTADOS"
docker-compose exec web python analyze_test_report.py

# 9. Mostrar relatório JSON (primeiras linhas)
print_header "📄 RELATÓRIO GERADO"
print_status "Primeiras linhas do relatório JSON:"
docker-compose exec web head -20 api_test_report.json

# 10. Opções pós-execução
print_header "📋 OPÇÕES DISPONÍVEIS"
echo "Para ver o relatório completo:"
echo "  docker-compose exec web cat api_test_report.json | python -m json.tool"
echo ""
echo "Para acessar o container interativamente:"
echo "  docker-compose exec web bash"
echo ""
echo "Para ver logs da aplicação:"
echo "  docker-compose logs web"
echo ""
echo "Para parar os containers:"
echo "  docker-compose down"
echo ""
echo "Para acessar a API diretamente:"
echo "  curl http://localhost:8000/api/"
echo ""

# 11. Verificar se quer manter containers rodando
read -p "🤔 Manter containers rodando? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Parando containers..."
    docker-compose down
    print_status "Containers parados"
else
    print_status "Containers mantidos rodando"
    print_warning "Lembre-se de executar 'docker-compose down' quando terminar"
    echo ""
    echo "🌐 API disponível em: http://localhost:8000"
    echo "📚 Documentação em: http://localhost:8000/api/docs/"
fi

print_status "Simulação concluída! ✅"
