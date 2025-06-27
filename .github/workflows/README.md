# 🚀 Testes Automatizados - Top Pet System

Este diretório contém os workflows do GitHub Actions para automação de testes e CI/CD do projeto Top Pet System.

## 📋 Workflows Disponíveis

### 1. **ci.yml** - Pipeline Principal de CI/CD
**Execução:** A cada push/PR nas branches `main` e `develop`

**Funcionalidades:**
- ✅ Testes unitários e de integração
- 🔍 Análise de código com flake8
- 📊 Relatório de cobertura de testes
- 🔒 Verificação de segurança (safety, bandit)
- 🐳 Build e teste de container Docker
- 📈 Upload de métricas para Codecov

### 2. **pr-tests.yml** - Testes para Pull Requests
**Execução:** Em todos os PRs abertos

**Funcionalidades:**
- 🧪 Execução completa de testes
- 📊 Comentário automático com cobertura de código
- ⚡ Feedback rápido para desenvolvedores

### 3. **matrix-tests.yml** - Testes em Múltiplas Versões
**Execução:** Semanal (segunda-feira, 2h UTC) ou manual

**Funcionalidades:**
- 🐍 Testa em Python 3.9, 3.10, 3.11, 3.12
- 🎯 Testa em Django 4.1, 4.2, 5.0
- 🔄 Matriz de compatibilidade

## 🛠️ Scripts Locais

### Para Linux/macOS:
```bash
cd backend
chmod +x run_tests.sh
./run_tests.sh --all
```

### Para Windows:
```powershell
cd backend
.\run_tests.ps1 -TestType all
```

## 📊 Opções de Teste

| Comando | Descrição |
|---------|-----------|
| `--all` | Executa todos os testes e verificações |
| `--unit` | Apenas testes unitários |
| `--integration` | Apenas testes de integração |
| `--coverage` | Testes com relatório de cobertura |
| `--pytest` | Executa com pytest |
| `--lint` | Apenas verificação de código |

## 🔧 Configuração Local

### Pré-requisitos:
1. Python 3.11+
2. PostgreSQL (para testes de integração)
3. Docker (opcional, para testes completos)

### Instalação:
```bash
cd backend
pip install -r requirements.txt
```

### Configuração do Banco de Dados:
```bash
# Criar banco de teste
createdb top_pet_test

# Executar migrações
python manage.py migrate
```

## 📈 Métricas e Relatórios

### Cobertura de Código:
- **Meta mínima:** 80%
- **Meta para novos códigos:** 90%
- **Relatórios:** `htmlcov/index.html`

### Qualidade do Código:
- **Linter:** flake8
- **Complexidade máxima:** 10
- **Tamanho de linha:** 127 caracteres

### Segurança:
- **Safety:** Verificação de vulnerabilidades em dependências
- **Bandit:** Análise de segurança do código Python

## 🚨 Troubleshooting

### Erro: "Database connection failed"
```bash
# Verificar se PostgreSQL está rodando
pg_isready

# Criar banco de teste se não existir
createdb top_pet_test
```

### Erro: "Module not found"
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Permission denied" (Linux/macOS)
```bash
# Dar permissão de execução ao script
chmod +x run_tests.sh
```

## 🔄 Integração Contínua

Os workflows são executados automaticamente quando:

1. **Push para main/develop:** Executa pipeline completo
2. **Abertura de PR:** Executa testes e análise de cobertura
3. **Agenda semanal:** Testa compatibilidade com diferentes versões
4. **Manual:** Pode ser executado a qualquer momento

## 📝 Contribuindo

Ao contribuir com o projeto:

1. ✅ Execute os testes localmente antes do commit
2. 📊 Mantenha a cobertura de testes acima de 80%
3. 🔍 Garanta que o código passa no flake8
4. 🔒 Verifique se não há vulnerabilidades de segurança

## 🔗 Links Úteis

- [Documentação do pytest](https://docs.pytest.org/)
- [Documentação do Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Coverage.py](https://coverage.readthedocs.io/)