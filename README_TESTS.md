# Configuração de Testes - Top Pet System

## Estrutura Normalizada para Testes

O sistema foi configurado para usar **SQLite em memória** para TODOS os tipos de testes, proporcionando máxima velocidade e simplicidade.

### Tipos de Testes Suportados

Todos os seguintes tipos de testes utilizam a mesma configuração otimizada:

1. **Testes Rápidos** - Testes básicos de funcionalidade
2. **Testes de Validação** - Validação de regras de negócio
3. **Testes de Unidade** - Testes isolados de componentes
4. **Testes de Integração** - Testes de integração entre módulos

### Configuração do Banco de Dados

- **Produção/API**: PostgreSQL (configurado via Docker Compose)
- **Todos os Testes**: SQLite em memória (`:memory:`)

### Vantagens do SQLite em Memória

✅ **Velocidade**: Execução extremamente rápida dos testes
✅ **Simplicidade**: Não requer configuração de servidor de banco
✅ **Isolamento**: Cada execução de teste inicia com banco limpo
✅ **Portabilidade**: Funciona em qualquer ambiente sem dependências externas
✅ **Sem Persistência**: Dados não são mantidos entre execuções

### Como Executar os Testes

#### 1. Testes da Simulação CRUD (Validação da API)
```bash
# Via Docker Compose
docker-compose exec web python test_api_simulation.py

# Localmente (após configurar ambiente)
python test_api_simulation.py
```

#### 2. Testes Unitários com Django
```bash
# Via Docker Compose
docker-compose exec web python manage.py test

# Localmente
python manage.py test
```

#### 3. Testes com Pytest
```bash
# Via Docker Compose
docker-compose exec web pytest

# Localmente
pytest
```

#### 4. Testes com Coverage
```bash
# Via Docker Compose
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report

# Localmente
coverage run --source='.' manage.py test
coverage report
```

### Configurações Específicas de Teste

O arquivo `top_pet/settings_test.py` contém:

- SQLite em memória como banco principal
- Hashers MD5 para velocidade
- Logs reduzidos (apenas ERRORs)
- Cache em memória
- Email backend de console
- Migrações desabilitadas para apps básicos do Django

### Estrutura de Arquivos

```
backend/
├── top_pet/
│   ├── settings.py          # Configurações principais (PostgreSQL)
│   └── settings_test.py     # Configurações de teste (SQLite)
├── test_api_simulation.py   # Simulação CRUD completa
├── setup_database.py       # Setup inicial do banco
└── requirements.txt        # Dependências (sem MySQL)
```

### Mudanças Implementadas

- ❌ **Removido**: MySQL e mysqlclient
- ❌ **Removido**: Configurações complexas de banco para testes  
- ❌ **Removido**: Docker container MySQL
- ✅ **Adicionado**: SQLite em memória para todos os testes
- ✅ **Adicionado**: Configurações otimizadas de performance
- ✅ **Adicionado**: Documentação clara da estrutura

### Variáveis de Ambiente

O arquivo `.env` agora contém apenas:

```env
# PostgreSQL para API
POSTGRES_NAME=top_pet_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
DB_PORT=5432

# Testes automaticamente usam SQLite em memória
# Não necessita configuração adicional
```

### Execução no CI/CD

Os testes no GitHub Actions executarão automaticamente com SQLite em memória, sem necessidade de configuração adicional de banco de dados.

### Troubleshooting

#### Erro de importação do mysqlclient
Se ainda houver erros relacionados ao MySQL, verifique:
1. `requirements.txt` não deve conter `mysqlclient`
2. `settings.py` não deve referenciar configurações MySQL
3. Limpe o cache: `docker-compose down && docker-compose build --no-cache`

#### Banco não existe
SQLite em memória é criado automaticamente. Se houver problemas:
1. Execute migrações: `python manage.py migrate`
2. Crie superusuário: `python setup_database.py`
