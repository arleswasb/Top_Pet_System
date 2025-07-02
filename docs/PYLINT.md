# Pipeline de CI/CD - Pylint e Testes com Cobertura

## Configuração do Pylint

Este projeto utiliza Pylint para análise estática de código Python, configurado para reportar apenas **erros críticos** e ignorar problemas de formatação e estilo.

### Arquivos de Configuração

1. **`.github/workflows/ci-pylint.yml`** - Pipeline do GitHub Actions
2. **`backend/.pylintrc`** - Configurações do Pylint

### Configurações Ignoradas

O Pylint está configurado para ignorar os seguintes tipos de problemas:

#### Formatação e Estilo
- `line-too-long` - Linhas muito longas
- `trailing-whitespace` - Espaços em branco no final das linhas
- `missing-docstring` - Documentação ausente
- `invalid-name` - Nomes de variáveis inválidos

#### Importações
- `unused-import` - Importações não utilizadas
- `wildcard-import` - Importações com *
- `unused-wildcard-import` - Importações * não utilizadas
- `wrong-import-position` - Posição incorreta de importações
- `imported-auth-user` - Importação do modelo User do Django

#### Complexidade
- `too-many-locals` - Muitas variáveis locais
- `too-many-arguments` - Muitos argumentos
- `too-many-instance-attributes` - Muitos atributos de instância
- `too-many-branches` - Muitas ramificações
- `too-many-statements` - Muitas declarações

#### Django Específico
- `no-member` - Membros não encontrados (Django fields)
- `import-error` - Erros de importação (Django modules)

### O que o Pylint Reporta

O pipeline reporta apenas **erros críticos** que podem causar falhas na execução:

- Erros de sintaxe
- Referências a variáveis não definidas
- Erros de indentação críticos
- Problemas de lógica que impedem execução

## Testes com Cobertura

### Instalação das Dependências

Para executar testes com cobertura, instale as dependências necessárias:

```bash
cd backend
pip install coverage pytest-cov
```

### Execução de Testes com Cobertura

#### Django Test Runner com Coverage

```bash
cd backend

# Execução básica com relatório de cobertura
coverage run manage.py test

# Gerar relatório no terminal
coverage report

# Gerar relatório HTML detalhado
coverage html

# Gerar relatório XML (para CI/CD)
coverage xml

# Executar testes de um app específico
coverage run manage.py test pets

# Combinar execução e relatório
coverage run manage.py test && coverage report
```

#### Configuração Avançada

Crie um arquivo `.coveragerc` no diretório `backend/`:

```ini
[run]
source = .
omit = 
    */migrations/*
    */venv/*
    */env/*
    manage.py
    */settings/*
    */wsgi.py
    */asgi.py
    */tests/*
    */test_*.py
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError

[html]
directory = htmlcov
```

#### Exemplos de Comandos Completos

```bash
# Teste completo com relatório HTML
coverage run --source='.' manage.py test
coverage html
# Abrir htmlcov/index.html no navegador

# Teste com filtro de cobertura mínima
coverage run manage.py test
coverage report --fail-under=80

# Teste de apps específicos
coverage run manage.py test pets users
coverage report --include="pets/*,users/*"

# Relatório resumido por arquivo
coverage report --show-missing

# Relatório detalhado em JSON
coverage json
```

### Pipeline de CI/CD com Cobertura

#### GitHub Actions

```yaml
# .github/workflows/test-coverage.yml
name: Tests with Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install coverage
    
    - name: Run tests with coverage
      run: |
        cd backend
        coverage run manage.py test
        coverage xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: unittests
        name: codecov-umbrella
```

### Métricas de Cobertura

#### Interpretação dos Resultados

- **Lines**: Linhas de código cobertas
- **Missing**: Linhas não cobertas pelos testes
- **Cover**: Percentual de cobertura
- **Missing lines**: Números das linhas específicas não cobertas

#### Metas de Cobertura

- **Mínimo aceitável**: 70%
- **Bom**: 80-90%
- **Excelente**: 90%+

### Relatórios Visuais

#### Relatório HTML

```bash
coverage html
# Abrir htmlcov/index.html
```

O relatório HTML oferece:
- Visão geral da cobertura por arquivo
- Detalhamento linha por linha
- Identificação visual de código não coberto
- Métricas por função/classe

#### Integração com IDEs

**VS Code**: Extensão Coverage Gutters
**PyCharm**: Built-in coverage support

### Scripts Úteis

#### Makefile para Automação

```makefile
# Makefile no diretório backend/
test:
	python manage.py test

test-coverage:
	coverage run manage.py test
	coverage report

test-html:
	coverage run manage.py test
	coverage html
	@echo "Relatório HTML gerado em htmlcov/index.html"

test-ci:
	coverage run manage.py test
	coverage xml
	coverage report --fail-under=70
```

#### Script Python

```python
# scripts/run_tests.py
import subprocess
import sys
import os

def run_tests_with_coverage():
    os.chdir('backend')
    
    # Executar testes
    result = subprocess.run(['coverage', 'run', 'manage.py', 'test'])
    if result.returncode != 0:
        sys.exit(1)
    
    # Gerar relatórios
    subprocess.run(['coverage', 'report'])
    subprocess.run(['coverage', 'html'])
    
    print("✅ Testes executados com sucesso!")
    print("📊 Relatório HTML disponível em backend/htmlcov/index.html")

if __name__ == "__main__":
    run_tests_with_coverage()
```

### Comandos Rápidos

```bash
# Setup inicial
pip install coverage

# Teste rápido
coverage run manage.py test && coverage report

# Teste com HTML
coverage run manage.py test && coverage html

# Teste apenas de um app
coverage run manage.py test pets && coverage report --include="pets/*"

# Verificar arquivos sem cobertura
coverage report --show-missing

# Falhar se cobertura < 80%
coverage report --fail-under=80
```

### Execução Local

Para executar o Pylint localmente:

```bash
cd backend
pylint --errors-only arquivo.py
```

### Pipeline de CI

O pipeline executa duas verificações:

1. **Verificação Principal** - Falha se encontrar erros críticos
2. **Relatório Completo** - Sempre executa para monitoramento (não falha)

### Benefícios

- ✅ Detecta apenas problemas que realmente importam
- ✅ Não bloqueia desenvolvimento por questões de estilo
- ✅ Foco na qualidade funcional do código
- ✅ Pipeline rápido e eficiente
- ✅ Configuração padronizada para todo o projeto
- ✅ Monitoramento contínuo da qualidade dos testes
- ✅ Identificação de código não testado
- ✅ Relatórios visuais detalhados
- ✅ Integração com ferramentas de CI/CD
