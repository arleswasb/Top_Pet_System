#!/bin/bash

# Script para executar testes localmente
# Usage: ./run_tests.sh [--coverage] [--unit] [--integration] [--all]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    print_error "Este script deve ser executado no diretório backend/"
    exit 1
fi

# Configurar variáveis de ambiente para teste
export DJANGO_SETTINGS_MODULE=top_pet.settings
export DEBUG=True
export SECRET_KEY=test-secret-key

# Função para executar migrações
run_migrations() {
    print_status "Executando migrações..."
    python manage.py migrate --run-syncdb
}

# Função para executar testes unitários
run_unit_tests() {
    print_status "Executando testes unitários..."
    python manage.py test pets.tests_unidade --verbosity=2
}

# Função para executar testes de integração
run_integration_tests() {
    print_status "Executando testes de integração..."
    python manage.py test agendamentos.tests_integracao --verbosity=2
}

# Função para executar todos os testes Django
run_django_tests() {
    print_status "Executando todos os testes Django..."
    python manage.py test --verbosity=2
}

# Função para executar testes com pytest
run_pytest_tests() {
    print_status "Executando testes com pytest..."
    pytest --verbose --tb=short
}

# Função para executar testes com coverage
run_coverage_tests() {
    print_status "Executando testes com coverage..."
    coverage run --source='.' manage.py test
    coverage report --show-missing
    coverage html
    print_status "Relatório de coverage HTML gerado em htmlcov/index.html"
}

# Função para verificar código com flake8
run_linting() {
    print_status "Verificando código com flake8..."
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
}

# Função principal
main() {
    print_status "Iniciando testes do Top Pet System..."
    
    # Instalar dependências se necessário
    print_status "Verificando dependências..."
    pip install -q coverage pytest-cov flake8
    
    # Executar migrações
    run_migrations
    
    # Processar argumentos
    case "${1:-all}" in
        "--unit")
            run_unit_tests
            ;;
        "--integration")
            run_integration_tests
            ;;
        "--coverage")
            run_coverage_tests
            ;;
        "--pytest")
            run_pytest_tests
            ;;
        "--lint")
            run_linting
            ;;
        "--all"|"")
            run_linting
            run_django_tests
            run_pytest_tests
            run_coverage_tests
            ;;
        *)
            print_error "Opção inválida: $1"
            echo "Uso: $0 [--coverage] [--unit] [--integration] [--pytest] [--lint] [--all]"
            exit 1
            ;;
    esac
    
    print_status "Testes concluídos com sucesso!"
}

# Executar função principal
main "$@"
