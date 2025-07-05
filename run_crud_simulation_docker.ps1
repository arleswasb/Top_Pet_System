# Script PowerShell para executar simulação CRUD com Docker Compose
# Usage: .\run_crud_simulation_docker.ps1

# Configurar para parar em erro
$ErrorActionPreference = "Stop"

# Função para prints coloridos
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

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Blue
    Write-Host $Message -ForegroundColor Blue
    Write-Host "===================================================" -ForegroundColor Blue
    Write-Host ""
}

# Verificar se docker-compose está disponível
try {
    docker-compose --version | Out-Null
} catch {
    Write-Error "docker-compose não está instalado ou não está no PATH"
    exit 1
}

Write-Header "🐳 SIMULAÇÃO CRUD TOP PET SYSTEM - DOCKER COMPOSE"

# 1. Parar containers existentes
Write-Status "Parando containers existentes..."
try {
    docker-compose down -v 2>$null
} catch {
    # Ignorar erro se não há containers
}

# 2. Construir e iniciar containers
Write-Status "Construindo e iniciando containers..."
docker-compose up -d --build

# 3. Aguardar containers ficarem prontos
Write-Status "Aguardando containers ficarem prontos..."
Start-Sleep -Seconds 10

# Verificar se containers estão rodando
$containersUp = docker-compose ps --filter "status=running" --quiet
if (-not $containersUp) {
    Write-Error "Containers não estão rodando corretamente"
    docker-compose logs
    exit 1
}

# 4. Aguardar banco de dados ficar pronto
Write-Status "Aguardando PostgreSQL ficar pronto..."
$timeout = 60
$elapsed = 0
do {
    try {
        docker-compose exec -T db pg_isready -U user -d top_pet_db 2>$null
        if ($LASTEXITCODE -eq 0) { break }
    } catch {}
    Start-Sleep -Seconds 2
    $elapsed += 2
} while ($elapsed -lt $timeout)

if ($elapsed -ge $timeout) {
    Write-Error "Timeout aguardando PostgreSQL"
    docker-compose logs db
    exit 1
}

# 5. Executar migrações
Write-Status "Executando migrações..."
docker-compose exec -T web python manage.py migrate --verbosity=0

# 6. Criar dados básicos necessários
Write-Status "Criando dados básicos..."
$pythonScript = @"
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
"@

docker-compose exec -T web python -c $pythonScript

# 7. Executar simulação CRUD
Write-Header "🚀 EXECUTANDO SIMULAÇÃO CRUD"
docker-compose exec web python test_api_simulation.py

# 8. Analisar resultados
Write-Header "📊 ANÁLISE DOS RESULTADOS"
docker-compose exec web python analyze_test_report.py

# 9. Mostrar relatório JSON (primeiras linhas)
Write-Header "📄 RELATÓRIO GERADO"
Write-Status "Primeiras linhas do relatório JSON:"
docker-compose exec web python -c "
import json
with open('api_test_report.json', 'r') as f:
    data = json.load(f)
print(f'Total de testes: {data.get(\"total_tests\", 0)}')
print(f'Sucessos: {data.get(\"passed\", 0)}')
print(f'Falhas: {data.get(\"failed\", 0)}')
print(f'Duração total: {data.get(\"total_duration\", 0):.3f}s')
"

# 10. Opções pós-execução
Write-Header "📋 OPÇÕES DISPONÍVEIS"
Write-Host "Para ver o relatório completo:"
Write-Host "  docker-compose exec web python -m json.tool api_test_report.json" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para acessar o container interativamente:"
Write-Host "  docker-compose exec web bash" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver logs da aplicação:"
Write-Host "  docker-compose logs web" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para parar os containers:"
Write-Host "  docker-compose down" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para acessar a API diretamente:"
Write-Host "  Invoke-WebRequest http://localhost:8000/api/" -ForegroundColor Cyan
Write-Host ""

# 11. Verificar se quer manter containers rodando
$response = Read-Host "🤔 Manter containers rodando? (y/N)"
if ($response -match '^[Yy]$') {
    Write-Status "Containers mantidos rodando"
    Write-Warning "Lembre-se de executar 'docker-compose down' quando terminar"
    Write-Host ""
    Write-Host "🌐 API disponível em: http://localhost:8000" -ForegroundColor Green
    Write-Host "📚 Documentação em: http://localhost:8000/api/docs/" -ForegroundColor Green
} else {
    Write-Status "Parando containers..."
    docker-compose down
    Write-Status "Containers parados"
}

Write-Status "Simulação concluída! ✅"
