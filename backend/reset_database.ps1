# Script para resetar o banco de dados do projeto Top Pet System
# Este script remove o banco atual e recria tudo do zero

Write-Host "🔄 Iniciando reset do banco de dados..." -ForegroundColor Yellow

# Verificar se estamos no diretório correto
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Erro: Execute este script no diretório backend onde está o manage.py" -ForegroundColor Red
    exit 1
}

# 1. Parar qualquer processo que possa estar usando o banco
Write-Host "📋 Passo 1: Verificando processos..." -ForegroundColor Cyan

# 2. Remover o arquivo do banco de dados SQLite
if (Test-Path "db.sqlite3") {
    Write-Host "🗑️  Passo 2: Removendo banco de dados antigo..." -ForegroundColor Cyan
    try {
        Remove-Item "db.sqlite3" -Force
        Write-Host "✅ Banco de dados removido com sucesso!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Erro ao remover banco: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "💡 Certifique-se de que nenhum processo está usando o banco (feche o Django, PyCharm, etc.)" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "ℹ️  Banco de dados não encontrado (talvez já tenha sido removido)" -ForegroundColor Yellow
}

# 3. Remover arquivos de migração (exceto __init__.py e arquivos iniciais necessários)
Write-Host "🗑️  Passo 3: Limpando migrações antigas..." -ForegroundColor Cyan

$apps = @("agendamentos", "pets", "users", "prontuarios", "configuracao")

foreach ($app in $apps) {
    if (Test-Path "$app\migrations") {
        Write-Host "   Limpando migrações de $app..." -ForegroundColor Gray
        
        # Remove todos os arquivos .py exceto __init__.py
        Get-ChildItem "$app\migrations\*.py" | Where-Object { $_.Name -ne "__init__.py" } | Remove-Item -Force
        
        # Remove cache do Python
        if (Test-Path "$app\migrations\__pycache__") {
            Remove-Item "$app\migrations\__pycache__" -Recurse -Force
        }
    }
}

# 4. Remover cache geral do Python
Write-Host "🗑️  Passo 4: Limpando cache do Python..." -ForegroundColor Cyan
if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
}

# Remover cache dos apps
foreach ($app in $apps) {
    if (Test-Path "$app\__pycache__") {
        Remove-Item "$app\__pycache__" -Recurse -Force
    }
}

# 5. Criar novas migrações
Write-Host "🔄 Passo 5: Criando novas migrações..." -ForegroundColor Cyan

try {
    python manage.py makemigrations
    if ($LASTEXITCODE -ne 0) {
        throw "Erro ao criar migrações"
    }
    Write-Host "✅ Migrações criadas com sucesso!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro ao criar migrações: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 6. Aplicar migrações
Write-Host "🔄 Passo 6: Aplicando migrações..." -ForegroundColor Cyan

try {
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        throw "Erro ao aplicar migrações"
    }
    Write-Host "✅ Migrações aplicadas com sucesso!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro ao aplicar migrações: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 7. Criar superusuário (opcional)
Write-Host "👤 Passo 7: Criar superusuário (opcional)..." -ForegroundColor Cyan
$createSuperuser = Read-Host "Deseja criar um superusuário agora? (s/N)"

if ($createSuperuser -eq "s" -or $createSuperuser -eq "S" -or $createSuperuser -eq "sim") {
    try {
        python manage.py createsuperuser
    }
    catch {
        Write-Host "⚠️  Superusuário não foi criado. Você pode criá-lo depois com: python manage.py createsuperuser" -ForegroundColor Yellow
    }
}

# 8. Limpar logs antigos (opcional)
Write-Host "🗑️  Passo 8: Limpando logs antigos..." -ForegroundColor Cyan
if (Test-Path "logs") {
    Get-ChildItem "logs\*.log" | Remove-Item -Force
    Write-Host "✅ Logs limpos!" -ForegroundColor Green
}

# 9. Limpar arquivos de mídia (opcional)
$clearMedia = Read-Host "Deseja limpar todos os arquivos de mídia/uploads? (s/N)"
if ($clearMedia -eq "s" -or $clearMedia -eq "S" -or $clearMedia -eq "sim") {
    if (Test-Path "media") {
        Write-Host "🗑️  Limpando arquivos de mídia..." -ForegroundColor Cyan
        Get-ChildItem "media" -Recurse | Remove-Item -Force -Recurse
        Write-Host "✅ Arquivos de mídia limpos!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🎉 Reset do banco de dados concluído com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Resumo do que foi feito:" -ForegroundColor White
Write-Host "   ✅ Banco de dados SQLite removido" -ForegroundColor Green
Write-Host "   ✅ Migrações antigas removidas" -ForegroundColor Green
Write-Host "   ✅ Cache do Python limpo" -ForegroundColor Green
Write-Host "   ✅ Novas migrações criadas e aplicadas" -ForegroundColor Green
Write-Host "   ✅ Novo banco de dados criado" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Agora você pode executar o servidor com: python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
