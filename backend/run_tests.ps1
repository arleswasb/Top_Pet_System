# Script para executar testes localmente no Windows
# Usage: .\run_tests.ps1 [-TestType <unit|integration|coverage|pytest|lint|all>]

param(
    [Parameter(Position=0)]
    [ValidateSet("unit", "integration", "coverage", "pytest", "lint", "all")]
    [string]$TestType = "all"
)

# Função para imprimir mensagens coloridas
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Verificar se estamos no diretório correto
if (-not (Test-Path "manage.py")) {
    Write-Error "Este script deve ser executado no diretório backend/"
    exit 1
}

# Configurar variáveis de ambiente para teste
$env:DJANGO_SETTINGS_MODULE = "top_pet.settings"
$env:DEBUG = "True"
$env:SECRET_KEY = "test-secret-key"

# Função para executar migrações
function Run-Migrations {
    Write-Status "Executando migrações..."
    python manage.py migrate --run-syncdb
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha ao executar migrações"
        exit 1
    }
}

# Função para executar testes unitários
function Run-UnitTests {
    Write-Status "Executando testes unitários..."
    python manage.py test pets.tests_unidade --verbosity=2
}

# Função para executar testes de integração
function Run-IntegrationTests {
    Write-Status "Executando testes de integração..."
    python manage.py test agendamentos.tests_integracao --verbosity=2
}

# Função para executar todos os testes Django
function Run-DjangoTests {
    Write-Status "Executando todos os testes Django..."
    python manage.py test --verbosity=2
}

# Função para executar testes com pytest
function Run-PytestTests {
    Write-Status "Executando testes com pytest..."
    pytest --verbose --tb=short
}

# Função para executar testes com coverage
function Run-CoverageTests {
    Write-Status "Executando testes com coverage..."
    coverage run --source='.' manage.py test
    coverage report --show-missing
    coverage html
    Write-Status "Relatório de coverage HTML gerado em htmlcov/index.html"
}

# Função para verificar código com flake8
function Run-Linting {
    Write-Status "Verificando código com flake8..."
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
}

# Função principal
function Main {
    Write-Status "Iniciando testes do Top Pet System..."
    
    # Instalar dependências se necessário
    Write-Status "Verificando dependências..."
    pip install -q coverage pytest-cov flake8
    
    # Executar migrações
    Run-Migrations
    
    # Processar argumentos
    switch ($TestType) {
        "unit" {
            Run-UnitTests
        }
        "integration" {
            Run-IntegrationTests
        }
        "coverage" {
            Run-CoverageTests
        }
        "pytest" {
            Run-PytestTests
        }
        "lint" {
            Run-Linting
        }
        "all" {
            Run-Linting
            Run-DjangoTests
            Run-PytestTests
            Run-CoverageTests
        }
        default {
            Write-Error "Opção inválida: $TestType"
            Write-Host "Uso: .\run_tests.ps1 [-TestType <unit|integration|coverage|pytest|lint|all>]"
            exit 1
        }
    }
    
    Write-Status "Testes concluídos com sucesso!"
}

# Executar função principal
try {
    Main
}
catch {
    Write-Error "Erro durante execução dos testes: $_"
    exit 1
}
