@echo off
echo.
echo =====================================================
echo    RESET DO BANCO DE DADOS - TOP PET SYSTEM
echo =====================================================
echo.

REM Verificar se estamos no diretório correto
if not exist "manage.py" (
    echo ❌ ERRO: Execute este arquivo no diretório backend onde está o manage.py
    pause
    exit /b 1
)

echo ⚠️  ATENCAO: Este comando ira DELETAR COMPLETAMENTE o banco de dados atual!
echo Todos os dados serao perdidos permanentemente.
echo.
set /p confirm="Deseja continuar? Digite 'sim' para confirmar: "

if /i not "%confirm%"=="sim" (
    echo Operacao cancelada pelo usuario.
    pause
    exit /b 0
)

echo.
echo 🔄 Iniciando reset do banco de dados...
echo.

REM Remover banco de dados
if exist "db.sqlite3" (
    echo 🗑️  Removendo banco de dados antigo...
    del /f "db.sqlite3"
    if exist "db.sqlite3" (
        echo ❌ Erro ao remover banco. Feche todos os programas que possam estar usando o banco.
        pause
        exit /b 1
    )
    echo ✅ Banco removido com sucesso!
) else (
    echo ℹ️  Banco de dados nao encontrado
)

REM Remover migrações
echo 🗑️  Limpando migracoes antigas...
for %%d in (agendamentos pets users prontuarios configuracao) do (
    if exist "%%d\migrations" (
        echo    Limpando migracoes de %%d...
        for %%f in ("%%d\migrations\*.py") do (
            if not "%%~nxf"=="__init__.py" (
                del /f "%%f"
            )
        )
        if exist "%%d\migrations\__pycache__" (
            rmdir /s /q "%%d\migrations\__pycache__"
        )
    )
)

REM Remover cache
echo 🗑️  Limpando cache do Python...
if exist "__pycache__" rmdir /s /q "__pycache__"
for %%d in (agendamentos pets users prontuarios configuracao top_pet) do (
    if exist "%%d\__pycache__" (
        rmdir /s /q "%%d\__pycache__"
    )
)

REM Criar migrações
echo 🔄 Criando novas migracoes...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar migracoes
    pause
    exit /b 1
)
echo ✅ Migracoes criadas!

REM Aplicar migrações
echo 🔄 Aplicando migracoes...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Erro ao aplicar migracoes
    pause
    exit /b 1
)
echo ✅ Migracoes aplicadas!

REM Criar superusuário
echo.
set /p create_user="Deseja criar um superusuario agora? (s/N): "
if /i "%create_user%"=="s" (
    python manage.py createsuperuser
)

REM Limpar logs
echo 🗑️  Limpando logs...
if exist "logs" (
    del /f /q "logs\*.log" 2>nul
)

echo.
echo 🎉 Reset do banco de dados concluido com sucesso!
echo.
echo 📋 Resumo do que foi feito:
echo    ✅ Banco de dados SQLite removido
echo    ✅ Migracoes antigas removidas  
echo    ✅ Cache do Python limpo
echo    ✅ Novas migracoes criadas e aplicadas
echo    ✅ Novo banco de dados criado
echo.
echo 🚀 Agora voce pode executar: python manage.py runserver
echo.
pause
